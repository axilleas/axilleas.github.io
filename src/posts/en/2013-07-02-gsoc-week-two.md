Title: GSoC - Weekly update 2
Tags: gsoc, fedora, gitlab
Category: geek

Unfortunately this week hasn't been very productive due to lack of time. I managed
to package 5-6 more gems, but I haven't submit them in Bugzilla yet. As always, the
most difficult and time consuming task is to make all the test suites provided
with each gem pass. And believe me this isn't always easy. So, here is what I did
this week.

## Meeting GitLab devs

We arranged a google hangout and we talked about the progress I make.
They were kind enough to ask whether I need help with something. 
Then I got to meet in person [Sytse Sijbrandij][] and [Marin Jankovski][] 
during [Euruko 2013][euruko]. Really cool guys.

Our main concern was about the gems that are GitLab's forks and how we should
deal with them since it is very unlikely they get accepted into the official Fedora
repos. See next week TODOs about that matter.

## Wikification and versioning process

I started a wiki page on [GitLab][gl], listing all the [dependencies][] and their versions.
I said version**s** because we have to deal with version mismatch, [remember][gsoc-prop]?
I am working on a script to get them automatically on a table. So far, I can extract
GitLab's and upstream versions whereas I still need Fedora's. Here's how I do it.

### GitLab

gem versions are retrieved from [this][gl-deps] dictionary. Pretty simple.

### Upstream

Using [this][upstream] method by qeuerying the API of rubygems.org and iterrating
through the missing gems, I can get in a list of the latest gem versions.
 
### Fedora

There is this nice tool in ruby called [pkgwat][] which queries Fedora's repo
database. This is also used by [isitfedoraruby][], which unfortunately doesn't have
an API. This would make my work a lot easier.

So, I decided to give this a shot by first [packaging][] it. This is what I am learning
here, isn't it? I thought this would be a matter of time since it only depends on
one unpackaged gem, [sanitize][] (which ironically is needed by GitLab too).

*(And I just whipped out a mosquito. Where the hell are they going 14.30 in the afternoon?...)*

The process that I thought would take me 30 minutes top, still goes on.
You see, `pkgwat` has a fixed dependency on `nokogiri 1.5.5` whereas the latest
`sanitize 2.0.4` requires `nokogiri>=1.6.0`. On Fedora we have `nokogiri 1.5.9`.
Let me draw that for you.

![Dependency hell](|filename|/images/pkgwat.png)

Welcome to Gem dependency hell. The only way to install it is through
`gem install pkwat`...

## Package review

My first informal review in order to be sponsored as a packager was 
[rubygem-rugged][rugged]. I did all my homework and I tested the given
SPEC and SRPM with fedora-review, I built the rpm using both mock and rpmbuild 
and then ran rpmlint against the produced packages. I made a few notes of 
what I thought needed fixing and with some help from Vit[^cheat] I submited
my review.

## Package submission

Last week I submited for review [rubygem-timers][timers], this week it
is [rubygem-redis][redis]. One package a week you say? Dude are you
ever going to package all these gems? Well, submiting a package for review
in bugzilla takes some time, as I carefully check to follow the guidelines
as much as I can. The toughest part of it all are the testing suites.
A test may rely on other gems that are not in Fedora yet, so I try to package 
them as well. [Here][pkgs] you will find some packages I am working on. 
Most of them are not submited for review yet.


## TODOs for next week

- Get more packages finished
- Complete the version table in wiki
- Start porting gemfile.py into ruby (eventually)
- Continue writing the article about Rubygem packaging
- Talk to infra team to see how that forked-gem-packaging will go
- I am just a placeholder, nothing useful here, I just wanted to continue the stairs

[^cheat]: I actually did seek for some help in [Ruby-SIG][] ML :p

[Ruby-SIG]: https://lists.fedoraproject.org/pipermail/ruby-sig/2013-July/001373.html
[pkgs]: https://github.com/axilleas/fedora/tree/master/packages
[packaging]: https://github.com/axilleas/fedora/blob/master/packages/rubygem-pkgwat/rubygem-pkgwat.spec
[pkgwat]: https://rubygems.org/gems/pkgwat
[isitfedoraruby]: https://github.com/zuhao/isitfedoraruby/blob/master/app/models/rpm_importer.rb#L46
[upstream]: https://github.com/axilleas/gsoc/blob/master/gemfile.py#L83
[gl-deps]: https://github.com/axilleas/gsoc/blob/master/gemfile.py#L30
[gl]: https://fedoraproject.org/wiki/User:Axilleas/GitLab
[gsoc-prop]: https://fedoraproject.org/wiki/GSOC_2013/Student_Application_Axilleas/Gitlab%28463%29#Version_mismatch
[dependencies]: https://github.com/axilleas/gsoc/blob/master/rubygems_missing
[rugged]: https://bugzilla.redhat.com/show_bug.cgi?id=927374
[redis]: https://bugzilla.redhat.com/show_bug.cgi?id=978284
[timers]: https://bugzilla.redhat.com/show_bug.cgi?id=969877
[Sytse Sijbrandij]: https://github.com/dosire
[Marin Jankovski]: https://github.com/maxlazio
[euruko]: http://euruko2013.org/
[sanitize]: https://rubygems.org/gems/sanitize
