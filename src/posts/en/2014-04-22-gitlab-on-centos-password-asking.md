Title: GitLab on CentOS asks for password when using git push via ssh
Slug: centos-gitlab-asks-for-password-on-git-push
Tags: centos, gitlab, selinux
Category: geek
Lang: en

Seems there is an issue floating around when a user tries to push on their
GitLab CentOS installation. There are two ways one can push to a git repo.
Using their username:password through http and using their ssh key without
the need of a password. For example:

```bash
git push http://centos.local/axil/git.git master
```

will prompt for the GitLab username:password

whereas

```bash
git push git@centos.local:axil/git.git master
```

will push to the repo without the need of a password just using the ssh key
I [uploaded][ssh-key-upload] using the GitLab interface.

**Note:** Pushing via ssh usually requires that you have set up properly
your `.ssh/config` for the user you are pushing from. Mine entry for example
looks like:

```bash
Host centos.local
  User axil
  Hostname centos.local
  PreferredAuthentications publickey
  IdentityFile /home/axil/.ssh/id_rsa
```

If you have installed GitLab on CentOS/RHEL, you may not be able to push via ssh
and the reason is the restrictions SELinux has on `/home/git/.ssh/` directory.
In order to fix this problem, simply run as root:

```bash
restorecron -Rv /home/git/.ssh/
```

You can read more [here][centos-ssh].

The above fix has already taken its way upstream in the CentOS guide at the [gitlab-recipes][] repo.
If you find any other issues you are welcome to submit them in the bug tracker.

[gitlab-recipes]: https://gitlab.com/axil/gitlab-recipes/commit/ab3dd4b427b4b6e531eda5de0775ea1b56f577bb "Ensure the correct SELinux contexts are set on .ssh/"
[centos-ssh]: http://wiki.centos.org/HowTos/Network/SecuringSSH "Securing OpenSSH on CentOS"
[ssh-key-upload]: https://www.youtube.com/watch?v=54mxyLo3Mqk "Create and Add your SSH key to GitLab "
