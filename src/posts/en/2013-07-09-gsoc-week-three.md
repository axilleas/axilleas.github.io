Title: GSoC - Weekly update 3
Tags: gsoc, fedora, gitlab
Category: geek

Here is what I have been doing this week (more like the past 10 days).

## Work on packages

**sanitize** 
Not yet submitted to BZ as it needs nokogiri 1.6.0 whereas in Fedora
we still have 1.5.9. Will have to talk to the maintainer of nokogiri for an update.

**boostrap-sass**
Submitted in [Bugzilla][bz-bootstrap]. This is a tricky one as per the package guidelines,
as it ships with some javascript files that are distributed from [Twitter bootstrap][tb],
which are considered a bundle. And if you don't already know it, bundling is
prohibited by the [packaging guidelines][bundle-guide]. You can follow the discussion
in the Bugzilla.

- orm_adapter

- devise

## Gems and their versions in json format

As I've mentioned before, one of the main problems about packaging GitLab, is
the version mismatch between GitLab, Fedora and upstream gems. I have added some
more functions to my [script][] and now it saves the gems with their corresponding
version in a json format. There are three files: `gitlab.json`, `fedora.json` and 
 `upstream.json`. 
 
I haven't added a flag to those methods yet, so one has to run it through the python
interpreter for now. Here's how:

0) Install [python-bugzilla][] and [pkgwat.api][] if not already.
1) `git clone https://github.com/axilleas/gsoc.git && cd gsoc`
2) Start your python interpreter (I prefer ipython)
3) `import gemfile as g`
4) `dicts = g.populate_dicts()`
5) `[gitlab, fedora, upstream] = dicts`

It will take a couple of minutes since it uses pkgwat.api to query the Fedora
database for the gems in Rawhide, and rubygems.org for the upstream versions.
`dicts` is a tuple containing all three dictionaries. With the last command we
unpacked the dictionaries of the tuple. So now calling gitlab, you have the gitlab
dictionary.

**Note:** All methods are called using the runtime gems of the current version of 
GitLab, which are 143 for now. According to those gems we then search the Fedora
package database and quering rubygems.org's API.

## Version table in wiki

There is now a [table][] in the wiki for an easy reference about the versions
of gems. Where you see `None` it means it hasn't been packaged for Fedora yet.
This is now automatically accomplished by running the script. 

Further below is a list of the gems to be packaged. Those that are submitted to
Bugzilla are accompanied with a link to their review. I am working on automating
this process, it should be something similar to how the wiki table is generated.

Also, I modified the output a little bit bit to be more readable. For example:

  >------------------------------------------------------
  >Gitlab runtime gems  :  143
  >Gems in Fedora repos :  380
  >Common gems          :  64
  >To be packaged       :  79
  >Pending review in BZ :  11
  >When BZ go in repos  :  68
  >
  >Fedora will have 20.79 % more ruby packages, that is 459 gems in total.
  >------------------------------------------------------


## Talk to infra team to see how that forked-gem-packaging will go

GitLab devs won't 

## Rubygem packaging article

Half done, nothing commited yet I have everything local.

## TODO next week

- 
