Title: GSoC - Weekly update 5
Tags: gsoc, fedora, gitlab, packaging
Category: linux

I can't believe that a month has already passed! I keep learning new things, mostly
on packaging, and the cool fact is that many of them are through my Review Requests.
The discussion between the reviewer and the reviewee can sometimes be very productive
leading to learning new things I previously ignored.

This post would be a long one but I decided to split it up, because some sections
deserved there own space.

The first split is named [I got approved as a packager, now what?](|filename|2013-07-21-fedora-after-packager-approval.md)
and it refers to all new Fedora packagers :)

The second one is going to talk about maintaining an unofficial repo and I will
describe my workflow and the potential scripts that facilitate the whole process.

And here is the rest of my progress during the fifth week. 

[TOC]

## Packages

This is the first time that some packages of mine got approved:

1. [hashie][]
2. [bootstrap-sass][]
3. [timers][]


I am also working on [rubygem-rugged][] as a reviewer this time. This is much more
difficult than being the reviewee, since it needs a lot testing from your side
and a good understanding of the guidelines.

And of course there is a bunch of other gems I am working on but not ready to
submit yet. As always, my progress is noted in this [trello board][].

## How to package a Ruby gem - blog post status

As you may know, I am in the process of writing an article on how to package Ruby
gems in Fedora. This is the only type of package I have been dealing with for the
past months, so I am far from an avid packager in general. But, as a structure
and wiki freak I like to have everything in order, even understandable by completely
newbies, so this is going to be very comprehensive. Progress is being made :)

You can now watch the progress [here][ruby-post-trello].

## TODO next week

- Submit more packages
- Set up GitLab on a Fedora machine and check if packaged bundler works
- Take on reviews of packages concerning the gsoc project


[repo-create]: https://fedoraproject.org/wiki/Fedorapeople_Repos#Script_for_easy_create_tree_local_repo_directory
[gitlab repository]: http://repos.fedorapeople.org/repos/axilleas/gitlab/
[ruby-post-trello]:  https://trello.com/c/oGOKkvBn/6-weekly-blog-posts
[bootstrap-sass]: https://bugzilla.redhat.com/show_bug.cgi?id=982679
[hashie]: https://bugzilla.redhat.com/show_bug.cgi?id=985358
[timers]: https://bugzilla.redhat.com/show_bug.cgi?id=969877
[trello board]: https://trello.com/c/IOzzF6MQ/16-gem-packaging-phase-1
[unofficial repo]: http://repos.fedorapeople.org/repos/axilleas/gitlab/
[rubygem-rugged]: https://bugzilla.redhat.com/show_bug.cgi?id=927374
