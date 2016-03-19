Title: SELinux policy for nginx and GitLab unix socket in Fedora 19
Category: opensource
Tags: selinux, fedora, gitlab, unixsocket, nginx

The installation of GitLab in Fedora 19 went fine. I followed the official installation
guide with some deviations where necessary, mostly taken from the CentOS guide in
[gitlab-recipes][]. I setup nginx using the ssl [config][], and poked some holes
in [iptables][]. For systemd services I used [these files][systemd].

So, everything is set, configuration tests pass, services are started, nginx is started
and I finally point firefox to my FQDN (which by the way is fedora.axilleas.me, no secret)
just to see a big fat **502 Bad Gateway**. 

As wikipedia [suggests][wiki]:

  > **502 Bad Gateway**
  >
  > The server was acting as a gateway or proxy and received an invalid response from the upstream server.

Spot on! The server (nginx) is acting as a proxy and received an invalid response from the upstream server (unicorn).
But what was that invalid response?

I could reach `ip_addr:8080` at which unicorn was listening, but not through my fqdn which
nginx was serving. So there clearly was something wrong with nginx.

[TOC]

## Error hunting

So the first thing when such an error occurs is to look through the logs.

### Nginx

In `/var/log/nginx/gitlab_error.log` I could see this error repeating:

```
2013/08/26 21:43:01 [crit] 2597#0: *50 connect() to unix:/home/git/gitlab/tmp/sockets/gitlab.socket failed (13: Permission denied) while connecting to upstream, client 12.34.56.78, server: fedora.axilleas.me, request: "GET /users/sign_in HTTP/1.1", upstream: "http://unix:/home/git/gitlab/tmp/sockets/gitlab.socket:/users/sign_in", host: "fedora.axilleas.me"
```

So we got a permission denied while nginx is trying to connect to the unix socket of GitLab.
After some hours searching and reading answers in stackoverflow, it sroke to me to check
whether SELinux is to blame. I set it to permissive mode with `setenforce 0` and voila,
nginx was suddenly recieving requests.

### SELinux you crafty little blocker

I remembered the awesome introductory guide of [SELinux][centoselinux] at CentOS wiki,
which I had used when rewriting the [CentOS installation guide][centosinstall] for GitLab
and immediately started reading.

By default, SELinux log messages are written to `/var/log/audit/audit.log` via the Linux Auditing System `auditd`.
If the `auditd` daemon is not running, then messages are written to `/var/log/messages`. 
SELinux log messages are labeled with the *AVC* keyword so that they might be easily filtered from other messages, as with `grep`. 

So, by greping nginx in `/var/log/audit/audit.log` I found those relative AVC messages, which indicate indeed
a denial of nginx connection to `gitlab.socket`.

```
type=AVC msg=audit(1377542938.307:248364): avc:  denied  { write } for  pid=2597 comm="nginx" name="gitlab.socket" dev="vda1" ino=1180273 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:httpd_sys_content_t:s0 tclass=sock_file
type=AVC msg=audit(1377542938.307:248364): avc:  denied  { connectto } for  pid=2597 comm="nginx" path="/home/git/gitlab/tmp/sockets/gitlab.socket" scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:system_r:initrc_t:s0 tclass=unix_stream_socket
```

Using a tool called `audit2allow` we are able to clear the AVC messages. If you haven't got it
installed, it is shipped with the `policycoreutils-devel` package.

```
grep nginx /var/log/audit/audit.log | audit2allow
```

and the result is:

```
#============= httpd_t ==============

#!!!! This avc is allowed in the current policy
allow httpd_t http_cache_port_t:tcp_socket name_connect;

#!!!! This avc is allowed in the current policy
allow httpd_t httpd_log_t:file setattr;

#!!!! This avc is allowed in the current policy
allow httpd_t httpd_sys_content_t:sock_file write;

#!!!! This avc is allowed in the current policy
allow httpd_t initrc_t:unix_stream_socket connectto;

#!!!! This avc is allowed in the current policy
allow httpd_t user_home_dir_t:dir search;

#!!!! This avc is allowed in the current policy
allow httpd_t user_home_t:dir { search getattr };

#!!!! This avc is allowed in the current policy
allow httpd_t user_home_t:sock_file write;

#!!!! This avc is allowed in the current policy
allow httpd_t var_run_t:file { read write };
```

These are the policies that should be used with SELinux. Notice that `user_home` is essential
since GitLab's `APP_ROOT` is in `/home/git/`. Similarly, you notice a policy related to 
the denied socket connection: `unix_stream_socket connectto`.

## Create a custom SELinux policy module

After all the investigation we are closer to the solution. All we have to do is use `audit2allow`
to generate a set of policy rules that would allow the required actions. We can generate
a local nginx Type Enforcement policy file (nginx.te): 

```
grep nginx /var/log/audit/audit.log | audit2allow -m nginx > nginx.te
cat nginx.te


module nginx 1.0;

require {
	type var_run_t;
	type user_home_dir_t;
	type httpd_log_t;
	type httpd_t;
	type user_home_t;
	type httpd_sys_content_t;
	type initrc_t;
	type http_cache_port_t;
	class sock_file write;
	class unix_stream_socket connectto;
	class dir { search getattr };
	class file { read write setattr };
	class tcp_socket name_connect;
}

#============= httpd_t ==============

#!!!! This avc is allowed in the current policy
allow httpd_t http_cache_port_t:tcp_socket name_connect;
allow httpd_t httpd_log_t:file setattr;
allow httpd_t httpd_sys_content_t:sock_file write;
allow httpd_t initrc_t:unix_stream_socket connectto;

#!!!! This avc is allowed in the current policy
allow httpd_t user_home_dir_t:dir search;

#!!!! This avc is allowed in the current policy
allow httpd_t user_home_t:dir { search getattr };
allow httpd_t user_home_t:sock_file write;
allow httpd_t var_run_t:file { read write };
```

We are not done yet, as this is a file for review only. We can then go ahead and use audit2allow 
to make a custom policy module to allow these actions: 

```
grep nginx /var/log/audit/audit.log | audit2allow -M nginx
semodule -i nginx.pp
```

We can check the policy module loaded correctly by listing loaded modules with `semodule -l`.

After that, remember to enable SELinux again with `setenforce 1`.

## Add nginx to git group

Unrelated to this article, but it is also needed for nginx to access the unix socket.
First we add nginx to git group, and then we make sure the group that owns `/home/git/`
has read and execute permissions:

```
usermod -a -G git nginx
chmod g+rx /home/git/
```

## TL;DR

To fix all nginx 502 issues, as root run:

```
yum install -y policycoreutils-{python,devel}
grep nginx /var/log/audit/audit.log | audit2allow -M nginx
semodule -i nginx.pp
usermod -a -G git nginx
chmod g+rx /home/git/
```

## Integration of SELinux error messages with journald 

In a very [interesting article][journl], Dan Walsh explains how this whole process of error
hunting will be much easier with Fedora 20. I urge you to read it.

With the upcoming changes, the error would have appeared at systemd's status log:

```
systemctl status nginx
```

and the possible solutions with:

```
journalctl  -r -o verbose -u nginx.service
```

Pretty cool, huh?

[centoselinux]: http://wiki.centos.org/HowTos/SELinux
[centosinstall]: https://github.com/gitlabhq/gitlab-recipes/blob/master/install/centos/README.md
[gitlab-recipes]: https://github.com/gitlabhq/gitlab-recipes
[config]: https://github.com/gitlabhq/gitlab-recipes/blob/master/web-server/nginx/gitlab-ssl
[iptables]: https://github.com/gitlabhq/gitlab-recipes/tree/master/install/centos#8-configure-the-firewall
[systemd]: https://github.com/gitlabhq/gitlab-recipes/tree/master/init/systemd
[wiki]: http://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_Server_Error
[secustom]: http://wiki.centos.org/HowTos/SELinux#head-faa96b3fdd922004cdb988c1989e56191c257c01
[journl]: http://danwalsh.livejournal.com/65777.html
