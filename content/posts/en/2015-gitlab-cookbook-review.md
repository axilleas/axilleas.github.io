Title: GitLab Cookbook review
Slug: gitlab-cookbook-review
Tags: gitlab, book, review
Category: reviews
Lang: en
Date: 2015-02-28

I'm happy to see more books written for GitLab and I'm even more happy when those
books come from people that are active contributors.

A year ago I wrote about the [GitLab repository management]({filename}./2014-01-09-gitlab-repository-management-book-review.md) book.
This time it is written by a fellow teammate of the GitLab core team,
[Jeroen van Baarsen][]. Here is my review.

![GitLab Cookbook](/images/gitlab_cookbook_frontcover.png)

[TOC]

## Chapters

### Introduction and installation

In the first chapter you are introduced to the history of GitLab and the various
ways to install it on your server. Jeroen covers all three officially supported
options and that is a huge plus. Whether you decide to install GitLab manually,
use the omnibus packages or use Chef and the GitLab cookbook, it's all there.
Every method is explained thoroughly so pick your medicine and deploy GitLab in
no time.

### Explaining git

If you are a newcomer to the world of Git and GitLab you will find this chapter
a nice entry point to start using both of them. Generate your first key,
upload it to GitLab and create a test project to see them in action.
I really liked the fact that Jeroen also included a way to create SSH keys on
windows as well (although I am a linux fanboy :p).

You will learn vital git operations like cloning, working with branches,
rebasing, squashing your commits and all these via a hands-on mini workshop!

### Managing users, groups and permissions

As the author states:

> GitLab is based on user interaction, but you want to have some control over all
the users in your system.

As an administrator of your GitLab instance you need to know the basic ins and
outs, and that is users and groups control. In this chapter you will learn how
to create new users and groups, add other people to groups and assign them the
correct permissions.

One of the greatest features of GitLab (among tens of others...) is the branch
protection. Git has a force push flag (`-f`) that may result to unwanted
effects in your project. How to properly use this feature is also covered here.

The last recipes of this chapter are the configuration of a project's visibility
and the removal of users through the admin area.

For someone new to GitLab this chapter includes some concepts that are well
explained with images where necessary.

### Issue tracker and wiki

GitLab advertises itself as a collaboration tool, so working with people is of
utmost importance. The issue tracker and the wiki are two of those features
that make collaboration a breeze.

Jeroen covers the usage of the issue tracker, the merge requests feature as
well as the milestones. Again, if you are new to these terms which form a
a very well known workflow among developers, you are about to learn a lot.

Then there is the small things that make a developer's life easier like the
reference of issues in commits, etc. Learn how to close an issue when
referencing its number in your commit message and making a merge request, as
well as referencing your team members, other issues, commits, etc.

Finishing this chapter you will learn how to interact with the wiki by creating
pages and also how to locally edit them with gollum. I really enjoyed the gollum
part as it was something I had not attempted before :)

### Maintaining your GitLab instance

So far we have seen how to use the web interface of GitLab to interact with
projects, users and groups. Starting from this chapter you are presented to
some system administration work that is vital if you are the owner of the
GitLab server.

In this chapter you will learn how to update GitLab to its latest version using
the omnibus packages or performing a manual upgrade. To be fair, I expected to
see an upgrade method using the Chef cookbook, just to be on par with the
installation methods, but that is not that big a deal.

Performing an upgrade can sometimes lead to some unintended errors and here you
will learn to use the tools GitLab provides to troubleshoot such situations.

Backup is a critical component of system administration tasks and it could not
be missing from the book! Learn how to backup and restore properly your GitLab
data. Extra points given to the fact that cron is mentioned and explained how
to be used with the backup process.

### Webhooks, external services and the API

Here is something we rarely see in tutorials on the internet.
GitLab is very powerful in that it provides methods to do more than code
collaboration. It can interact with other external services via a plugin system.
Send messages to Slack, Campfire, recieve mails when a push is made, are some of
the many supported services.

Web hooks and system hooks are nicely explained with examples and it's a really
good start for someone who is unaware of them.

If you are keen on automating certain actions like project or user creation, you
most probably want to use a script or an automation tool to do it without
interacting with the web UI. Enter API.

GitLab provides a very robust API and Jeroen does a wonderful job explaining
the various actions you can perform. I won't go into details but you will learn
among others how to manage your projects and users via the API. All with good
examples and images where needed to have a nice visual.

### Using LDAP and OmniAuth providers

If you work to a company you probably have some internal authentication
mechanism like LDAP. You will be happy to know that GitLab supports LDAP out
of the box (well after some minimal configuration that is).

In this chapter you will learn how to set up your own LDAP server, adding users
to it and configuring GitLab to use LDAP.

**Note:** When the book was written, GitLab used to use a different method to
    declare the LDAP values in omnibus installations. The book's method is
    outdated as we now set the values in yaml format.
    See the [gitlab.rb.template][].

GitLab also comes with OmniAuth support, that is you can sign-up and create new
users by other authentication applications. GitHub is explained here.

### GitLab CI

> GitLab CI is a continuous integration solution made by the same team that made
GitLab. A CI system allows you to run automated unit tests on every commit, and
will warn you when a build is not successful. It is also possible to have a
healthy build deployed automatically.

In this chapter you will learn how to manually install the coordinator, the
heart of the GitLab CI system, a runner and how to link your first
GitLab project to the CI. All meticulously explained.

**Note:** Newer versions of the omnibus package [include the CI][ci], so there
    is no need to manually install it.

### Tips and tricks

The last chapter of the book deals with tips and tricks of GitLab. Here you will
learn about the anatomy of GitLab itself, the differences between the free,
open source edition and the enterprise one as well as some best practices like
the branch workflow.

Rest assured that you're not finished yet! You will also learn how to get
involved to the vibrant community of GitLab and where to ask for help.

## To sum up

Whether you are just entering the world of Git and GitLab[^worldofpain] or just
looking for ways to expand your knowledge on the stuff that make GitLab excel
in its field, this is the book for you. If I were to rate it I would give it
**9/10**. The lost point is because some parts are outdated but that's only
natural given the nature of the publishment of the book and the fast pace of
GitLab.

Well done my friend!

--> [Now go grab a copy!][copy] <--


[^worldofpain]: I couldn't help it :p <https://youtu.be/YedqV4Gl_us?t=1m34s>

[Jeroen van Baarsen]: http://www.jvanbaarsen.com/ "Jeroen van Baarsen Blog"
[gitlab.rb.template]: https://gitlab.com/gitlab-org/omnibus-gitlab/blob/484227e2dfe33f59e3683a5757be6842d7ce79d2/files/gitlab-config-template/gitlab.rb.template#L44
[ci]: https://about.gitlab.com/2014/11/04/gitlab-omnibus-packages-now-include-gitlab-ci/ "GitLab Omnibus packages now include GitLab CI"
[copy]: https://www.packtpub.com/application-development/gitlab-cookbook "GitLab Cookbook on Packt Publishing"
