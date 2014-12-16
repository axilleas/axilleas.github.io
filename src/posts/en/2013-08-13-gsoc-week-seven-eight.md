Title: GSoC - Weekly update 7 and 8
Tags: gsoc, fedora, gitlab, packaging
Category: opensource

The past week or so, I have been trying to package every gem GitLab needs, in Fedora 19.
This is something I should have done from the start, but better late than never.
Now that I have quite learnt the rubygem packaging process, I follow a certain
workflow that gets the job done pretty quickly (described below).

The [repo][] I had setup, now includes the majority of the gems needed for a working
GitLab instance.

Of course many of them do not pass the standards in order to submit to Bugzilla,
meaning there are some gems missing the license file, the tests are not shipped or
fail, etc. The only thing that is correct in all of them is the declaration of files
to be incuded in the final packaged gem, that is the `%files` and `%files doc` macros.

[TOC]

## Workflow of quick packaging

For the whole time I've been packaging gems, I use a VPS running Fedora 19. Luckily it is
a pretty strong machine (4GB RAM, 4 cpu) and building a rubygem in mock takes 1-3 minutes[^cloud].

In general, I first check in the [wiki table][] what's missing, and then build the next gem in line.
I have 2 screen windows open (among others): one pointing in `~/rpmbuild/SPECS/`
and the other to `~/rpmbuild/SRPMS/`. Here are the steps onwards.

On the first screen I run a simple [script][gemget] that downloads the gem file 
in `~/rpmbuild/SOURCES/` and then runs gem2rpm on it with the resulting spec 
saved in `~/rpmbuild/SPECS/`. I then open the spec with vim, open the url and 
check if the license tag is filled. If not, I check in the url for the license file. 

Inside vim, I save the changes with `:w` and run `:!rpmbuild -ba %`. Normally,
this will fail, which is good. We need the info provided by the `error: Installed (but unpackaged) file(s) found:`
I copy all these stuff in a temp file (I have geany open) and then I fix the
`%files` and `%files doc` macro accordingly. Save and run `:!rpmbuild -ba %`
again to check everything is in order. If the build exits with no error, I try
to make the tests work. I give myself 10-15 minutes topfor each gem, as I am
targeting to test the GitLab installation and not submit them to Bugzilla.
Of course during the whole process, I keep track what fails and what not, so
that I can come back later. You can see [here][builderrors] my progress.

After the build runs fine, I use `mock` to test that a package is not missing
from the BuildRequires. Exit the `rpmbuild` screen, enter `mock`, which is in
`~/rpmbuild/SRPMS/`, so with a simple `mock rubygem-foo-1.0-1.src.rpm` begins
the packaging process. If something breaks, back to `rpmbuild` screen, adjust
the spec, save it, run `:!rpmbuild -bs %` to just produce the srpm, exit screen,
enter `mock` screen, run `mock rubygem-foo-1.0-1.src.rpm` again. And the circle
goes on until I have a working rpm.

When the package builds fine in mock, I copy the produced rpms in `~/repo/gitlab/fedora-19/`
with `cp /var/lib/mock/fedora-19-x86_64/result/*rpm ~/repos/gitlab/fedora-19`.
From there, I move each package to its destined folder and using a modified [script][]
of [repo_update][] I sync the packages to my repo hosted on fedorapeople.org.

### Notes

Using of mock is of utter importance. Building in a clean chrooted environment,
you ensure that a package builds and installs cleanly without any dependencies missing,
on other machines as well.

The use of the repository is two-fold. Other than the default nature of the repo 
where you could easily install and test GitLab, it also serves as a building point 
where you have packages needed by other packages and so on, that are not yet in Fedora. 
Sure you could use `mock --init` as described [here][mock-init], but that is quite
a burden when there is a multiple dependency issue. For that purpose I made my 
mock default config being a copy of the `fedora-19-x86_64.cfg` plus the information of the
[fedora-gitlab.repo][]. 

0. `sudo cp /etc/mock/fedora-19-x86_64 /etc/mock/gitlab-x86_64.cfg`
1. `sudo vim /etc/mock/gitlab-x86_64.cfg`
2. Append the info of [fedora-gitlab.repo][] (be carefull of the `"""`, they must be last)
3. Repeat 1-3 for a `i686` config.
4. `sudo ln -s /etc/mock/gitlab-x86_64 /etc/mock/default.cfg` so that I don't have to
    repeatedly invoking the mock configs with the `-r` flag.

Ultimately, `gitlab-x86_64.cfg` looks like this:

    config_opts['root'] = 'fedora-19-x86_64'
    config_opts['target_arch'] = 'x86_64'
    config_opts['legal_host_arches'] = ('x86_64',)
    config_opts['chroot_setup_cmd'] = 'groupinstall buildsys-build'
    config_opts['dist'] = 'fc19'  # only useful for --resultdir variable subst

    config_opts['yum.conf'] = """
    [main]
    cachedir=/var/cache/yum
    debuglevel=1
    reposdir=/dev/null
    logfile=/var/log/yum.log
    retries=20
    obsoletes=1
    gpgcheck=0
    assumeyes=1
    syslog_ident=mock
    syslog_device=

    # repos

    [fedora]
    name=fedora
    mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=fedora-19&arch=x86_64
    failovermethod=priority

    [updates]
    name=updates
    mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f19&arch=x86_64
    failovermethod=priority

    [updates-testing]
    name=updates-testing
    mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=updates-testing-f19&arch=x86_64
    failovermethod=priority
    enabled=0

    [local]
    name=local
    baseurl=http://kojipkgs.fedoraproject.org/repos/f19-build/latest/x86_64/
    cost=2000
    enabled=0

    [fedora-debuginfo]
    name=fedora-debuginfo
    mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=fedora-debug-19&arch=x86_64
    failovermethod=priority
    enabled=0

    [updates-debuginfo]
    name=updates-debuginfo
    mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-debug-f19&arch=x86_64
    failovermethod=priority
    enabled=0

    [updates-testing-debuginfo]
    name=updates-testing-debuginfo
    mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=updates-testing-debug-f19&arch=x86_64
    failovermethod=priority
    enabled=0

    [fedora-gitlab]
    name=Unofficial GitLab repository for Fedora
    baseurl=http://repos.fedorapeople.org/repos/axilleas/gitlab/fedora-$releasever/$basearch/
    enabled=1
    skip_if_unavailable=1
    gpgcheck=0

    [fedora-gitlab-noarch]
    name=Unofficial GitLab repository for Fedora
    baseurl=http://repos.fedorapeople.org/repos/axilleas/gitlab/fedora-$releasever/noarch/
    enabled=1
    skip_if_unavailable=1
    gpgcheck=0

    [fedora-gitlab-source]
    name=Unofficial GitLab repository for Fedora - Source
    baseurl=http://repos.fedorapeople.org/repos/axilleas/gitlab/fedora-$releasever/SRPMS
    enabled=0
    skip_if_unavailable=1
    gpgcheck=0

    """


## Difficulties in gem versions

The most challenging aspect of my whole GSoC project is not how to package the 
~ 80 gems needed for GitLab at runtime, but how to coordinate GitLab-Fedora-Upstream
and their different versions of gems.

In this process, there are two key stoppers that need to be resolved.

1. For gems with versions: GitLab < Fedora, I will have to test if they properly work.
    Else, a gem with lower version should be packaged for Fedora.

2. For gems with versions: GitLab > Fedora, if GitLab == Upstream, it is easy to update by asking the maintainer to update, 
    BUT if Fedora < GitLab < Upstream , it is *hard*, as it is needed a version lower than the
    current upstream, and in Fedora we try to have the latest version. Of course
    that is debatable and if really needed, a gem with lower version than upstream
    could be submitted.

## TODO

- There are about 15 more gems to package
- Somehow deal with GitLab's forks
- Commit to github the specs i have built so far with propper commit messages
- Test in a gitlab-vagrant VM some new gem versions I built and submit PR with updated Gemfile
- Start packaging the GitLab app itself (get a clue from Gitorious)
- Check which gems are ok so far to submit to Bugzilla



[^cloud]: All that thanks to [okeanos][], a [GRNET][]'s public cloud service which provides cloud services to the whole Greek research and academic community. More info [here][synnefo].

[repo]: http://repos.fedorapeople.org/repos/axilleas/gitlab/fedora-19/
[wiki table]: https://fedoraproject.org/wiki/User:Axilleas/GitLab#Packages
[synnefo]: http://www.synnefo.org/
[okeanos]: https://okeanos.grnet.gr/home/
[GRNET]: https://www.grnet.gr/en/
[builderrors]: https://github.com/axilleas/gsoc/blob/master/packaging.md
[script]: https://github.com/axilleas/gsoc/blob/master/repo-update
[repo_update]: https://fedoraproject.org/wiki/Fedorapeople_Repos#Script_for_easy_repo_update
[mock-init]: https://fedoraproject.org/wiki/Using_Mock_to_test_package_builds#Building_packages_that_depend_on_packages_not_in_a_repository
[fedora-gitlab.repo]: http://repos.fedorapeople.org/repos/axilleas/gitlab/fedora-gitlab.repo
[gemget]: https://github.com/axilleas/gsoc/blob/master/gemget
