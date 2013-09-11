Title: GSoC - Weekly update 11 and 12
Tags: gsoc, fedora, gitlab, packaging
Category: linux

So far, I managed to [deploy GitLab][fedora] on a Fedora 19 machine using only packaged gems either from
the official repos or a [custom][repo] one I have created.
 
Below you will find some more info as well as the url of the testing environment. 
You can use/test it and report any issues [here][issues]. If anyone needs an admin account 
for further testing just let me know. Just bare in mind that you might see some 500 errors as I will be trying some things.

More or less, here is the workflow I followed:

1. Set up GitLab in a VM following the official installation guide and test everything works
1. `rm -rf /vendor/bundle`
3. Test with `bundle install --local RAILS_ENV=production`
4. See the dependency differences
2. Install with `yum` the gems in Gemfile
5. Replace in Gemfile/Gemfile.lock with Fedora versions
6. Repeat steps 3,4,5,6

For details on what is replaced see this [Gemfile.lock.diff][diff].
The systemd services I used can be found [here][systemd].
 
There are a lot to be done yet until this reaches to the official repos but that's a start.

## TODO

### Short term
- Write the gitlab.spec that will glue all the dependencies together

### Long term
- Commit as many specs as  possible to BZ.
- GitLab forks: one option is to patch upstream with GitLab's changes. Second but rather avoided is to to ask FPC for an exception and package the forks as they are.
- Coordinate efforts with Debian ruby team ([related discussion][debian])
- Deploy on rawhide: when GitLab supports rails 4. That depends on many dependencies gems as well.

### Longer term
- port to EPEL


[issues]: https://github.com/axilleas/gsoc/issues
[repo]: http://repos.fedorapeople.org/repos/axilleas/gitlab/fedora-19/
[fedora]: https://fedora.axilleas.me
[diff]: https://github.com/axilleas/gsoc/blob/master/Gemfile.lock.diff
[systemd]: https://github.com/axilleas/gsoc/tree/master/systemd
[debian]: http://debian.2.n7.nabble.com/Regarding-gitlab-td2843993.html 
