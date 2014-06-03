Title: GSoC - Weekly update 9 and 10
Tags: gsoc, fedora, gitlab, packaging
Category: linux

I've been busy the past two weeks with some personal stuff so I got a little behind.
Here's what happened in the GitLab front.

[TOC]

## Finish packaging remaining gems

Now, all (hopefully) runtime dependencies are packaged and pushed in my public [gitlab-repo][].
The majority of them are not ready for official submission in Bugzilla, but I kept track
of those that pass the standards in order to be submitted. Unfortunately they are only 5...

```
escape_utils
http_parser.rb
modernizr
yajl-ruby (already submitted https://bugzilla.redhat.com/show_bug.cgi?id=823351)
settingslogic
stamp
```

For now I have also packaged the forks as they need some more work to be accepted in Fedora.
[Here][forks] I have pointed out their differences with original gems.

## GitLab deploy

I deployed [GitLab in Fedora 19][glab] on a VPS following the standard installation, meaning all gems
are bundled under `vendor/bundle/`. You can visit it, but it may not be functional as I am now in the
process of replacing the bundled gems with the system ones. Expect more info on this in a following post.

## Coordinate packaging with Debian

In other news, I found out that Debian is also in the process of packaging GitLab, so I contacted them through
their [Ruby ML][debian-ruby] regarding this. If you follow the discussion you will understand that the main
problem for them is also how to package the forked gems. Hopefully we will come to a solution.

## TODO

- Build dummy `gitlab.spec` with all runtime `Requires` for easy test install
- Use `bundle install --local` and progressively test the required gems


[gitlab-repo]: http://repos.fedorapeople.org/repos/axilleas/gitlab/fedora-19/
[forks]: https://github.com/axilleas/gsoc/blob/master/packaging.md#gem-packaging-on-gitlab-forks
[debian-ruby]: http://debian.2.n7.nabble.com/Regarding-gitlab-td2843993.html
[glab]: https://fedora.axilleas.me
