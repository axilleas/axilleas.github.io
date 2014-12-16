Title: GSoC - Weekly update 3 and 4
Tags: gsoc, fedora, gitlab
Category: opensource

Here is what I have been doing the last two weeks.

[TOC]

## Work on packages

I ran gem2rpm on all gems and saved their specs in a [tmp][tmp-specs] folder
so that I can easily modify them later. I intend to split them in categories
according to the bundled gems in GitLab's [Gemfile][] that are needed for production.
Below are some gems that are either almost ready for Bugzilla or submitted. There
are a dozen more that I work with but haven't pushed any changes to github. Will
do soon.

### sanitize

Not yet submitted to BZ as it needs nokogiri 1.6.0 whereas in Fedora
we still have 1.5.9. Will have to talk to the maintainer of nokogiri for an update.

### boostrap-sass

Submitted in [Bugzilla][bz-bootstrap]. This is a tricky one as per the package guidelines,
as it ships with some javascript files that are distributed from [Twitter bootstrap][tb],
which are considered a bundle. And if you don't already know it, bundling is
prohibited by the [packaging guidelines][bundle-guide]. You can follow the discussion
in the Bugzilla. There is also an interesting discussion going on in packaging ML,
about web Assets/JavaScript guidelines and are proposed some [drafts][js-drafts].
This could probably alter the packaging structure of bootstrap-sass, but I don't
expect it anytime soon.

### orm_adapter

Some tests are skipped because they require some gems not yet packaged for Fedora,
but that is a [little acceptable][list-test]. This is a dependency of devise (see
below). To be submitted soon.

### devise

[Devise][] provides ready-made authentication and user management for rails
applications. It is a very popular rack application among the rails community, so
it'll be cool to get it into Fedora's repos :)
Submission is on the way along with orm_adapter.


## Gems and their versions in json format

As I've mentioned before, one of the main problems about packaging GitLab, is
the version mismatch between GitLab, Fedora and upstream gems. I have added some
more functions to my [script][] and now it saves the gems with their corresponding
version in a json format. There are three files: `gitlab.json`, `fedora.json` and 
 `upstream.json`. 
 
I haven't added a flag to those methods yet, so one has to run it through the python
interpreter for now. Here's how:


0. Install [python-bugzilla][] and [pkgwat.api][] if not already.
1. `git clone https://github.com/axilleas/gsoc.git && cd gsoc`
2. Start your python interpreter (I prefer ipython)
3. `import gemfile as g`
4. `dicts = g.populate_dicts()`
5. `[gitlab, fedora, upstream] = dicts`

It will take a couple of minutes since it uses pkgwat.api to query the Fedora
database for the gems in Rawhide, and rubygems.org for the upstream versions.
`dicts` is a tuple containing all three dictionaries. With the last command we
unpacked the dictionaries of the tuple. So now calling gitlab, you have the gitlab
dictionary and so on.

**Note:** All methods are called using the runtime gems of the current version of 
GitLab, which are 143 for now. According to those gems we then search the Fedora
package database and quering rubygems.org's API.

## Version table in wiki

There is now a [table][] in the wiki for an easy reference about the versions
of gems. Where you see `None` it means it hasn't been packaged for Fedora yet.
This is now [automatically][table-script] accomplished by running the script. 

Further below is a list of the gems to be packaged. Those that are submitted to
Bugzilla are accompanied with a link to their review. I am working on automating
this process, it should be something similar to how the wiki table is generated.

Also, I modified the output a little bit to be more readable. For example:

    ------------------------------------------------------
    Gitlab runtime gems  :  143
    Gems in Fedora repos :  380
    Common gems          :  64
    To be packaged       :  79
    Pending review in BZ :  11
    When BZ go in repos  :  68

    Fedora will have 20.79 % more ruby packages, that is 459 gems in total.
    ------------------------------------------------------

## Init repository

I have created a repository at [fedorapeople.org][] to start populating it with packages
I build, but take a long time to get to Fedora repos. This should be a good chance
to test the packages they make it to Rawhide.

Most gems come with a bundled test suite. Running tests during gem packaging
can sometimes be cumbersome but it is the only way to test that the gem really
works, at least according to the suite. To my experience, getting the tests run
requires a big amount of your time during package building, so in this test repo
expect to find many packages without their tests run. At least this is going to
be the case at the beginning.

## Rubygem packaging article

Half done, nothing commited yet, I have everything local. This takes more time
than I expected, as I want it to be easily understandable by people that don't
have a clue, but also a good guide for more experienced users. I am rather picky
and I read what I write many times, so yeah, this is going to take longer to finish.

## TODO next week

- Categorize gems according to their dependencies.
- Submit 5-10 more gems.
- Deploy GitLab on a Fedora server and test with some packaged gems. This is going to hit me hard I feel it :p
- Maybe write an unofficial guide of how to install GitLab in Fedora, haven't checked if there is a guide out in the internets.

[fedorapeople.org]: http://repos.fedorapeople.org/repos/axilleas/gitlab/
[js-drafts]: https://lists.fedoraproject.org/pipermail/packaging/2013-July/009304.html
[Gemfile]: https://github.com/gitlabhq/gitlabhq/blob/master/Gemfile#L11-L143
[list-test]: https://lists.fedoraproject.org/pipermail/ruby-sig/2013-July/001384.html
[Devise]: http://github.com/plataformatec/devise
[tmp-specs]: https://github.com/axilleas/fedora/tree/master/packages/tmp
[bz-bootstrap]: https://bugzilla.redhat.com/show_bug.cgi?id=982679
[bundle-guide]: https://fedoraproject.org/wiki/Packaging:Guidelines#Duplication_of_system_libraries
[tb]: https://github.com/twitter/bootstrap
[python-bugzilla]: https://fedorahosted.org/python-bugzilla/‎
[pkgwat.api]: http://pkgwat.readthedocs.org/en/latest/
[script]: https://github.com/axilleas/gsoc/blob/master/gemfile.py
[table]: https://fedoraproject.org/wiki/User:Axilleas/GitLab#Packages
[table-script]: https://github.com/axilleas/gsoc/blob/master/gemfile.py#L217
[tmp-specs]: https://github.com/axilleas/fedora/tree/master/packages/tmp
