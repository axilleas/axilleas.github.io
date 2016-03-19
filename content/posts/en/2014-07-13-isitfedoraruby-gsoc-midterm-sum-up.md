Title: isitfedoraruby gsoc midterm sum up
Slug: isitfedoraruby-gsoc-midterm-sum-up
Tags: fedora, gsoc, ruby, rails, webdev, isitfedoraruby
Category: opensource
Lang: en

This sums up my past month involvement with the project. A lot of reading in
between...

[TOC]

## Changelog

I added a changelog so that the changes are easily seen, so here it is (this week is v 0.9.1):

```
v 0.9.1

- Refactor rake tasks
- Source Code uri in fedorarpms, points to pkgs.fp.o gitweb
- Add first integration tests
- Retrieve commit data via Pkgwat
- Show name of last packager in fedorarpms#show
- Show last commit message in fedorarpms#show
- Show last commit date in fedorarpms#show
- Use api to fetch rawhide version instead of scrapping page
- Retrieve homepage via Pkgwat
- Fix duplication of dependencies in fedorarpms#show
- Do not show source url in rubygems#show if it is the same as the homepage
- Do not show source url in fedorarpms#show if it is the same as the homepage
- Split methods: versions, dependencies in fedorarpm model
- New rake tasks to import versions, dependencies and commits
- Show last packager in fedorarpms#show
- Show last commit message in fedorarpms#show
- Show last commit date in fedorarpms#show

v 0.9.0

- Remove unused code
  - Remove HistoricalGems model
  - Remove Build controller/view
  - Remove methods related to local spec/gem downloading
  - Remove empty helpers
  - Cleaned routes, removed unused ones
- Conform to ruby/rails style guide
- Maintainer field for packages are now using the fas_name
- Automatically fetch versions of Fedora by querying the pkgdb api
- Addded rake task to fetch rawhide version and store it in a file locally
- Show koji builds from supported Fedora versions only
- Bugs
  - Query bugs via api using pkgwat
  - Drop is_open from bugs table
  - Show only open Fedora bugs, exclude EPEL
- Hover over links to see full titles when truncated
- Rename builds table to koji_builds
- Added tests
  - Unit tests for models
- Added Github services
  - travis-ci
  - hound-ci
  - coveralls
  - gemnasium
- Development tools
  - shoulda-matchers
  - rspec
  - capybara
  - rack-mini-profiler
  - rubocop
  - factory_girl
  - annotate
  - railsroady
```

You should notice some version numbers. That's also a new addition and every
week I will deploy a new version, so eventually at some point in the end of the
summer, version 1.0.0 will be released.

Here are some nice stats from git log.

[Git stats][stats]: 91 commits / 4,662 ++ / 2,874 --

## Rails/Ruby style guide

Fixed arround 500 warnings that rubocop yielded.

## Tests

Added: unit tests for models.

Missing:
A bunch of code still needs testing, rspec is not enough to properly test api
calls. I will use [vcr][] and [webmock][] in the future to cover these tests.
Integration tests are also not complete yet.

## Bugs fixed

### wrong owners

Previously it parsed the spec file and checked the first email in the
changelog. Co-maintainers have also the ability to build a package and in
that case it shows wrong info. Another case is where a user changes their
email they are taken into account twice, so when hitting `/by_owner` not all
packages are shown. I was hit by this bug.

It now fetches the owner's fas name using [pkgwat][] which I use to sort
by owner.

### dependencies shown twice

The current implementation scraps the SPEC file of a rubygem via the [gitweb][]
and then stores the dependencies. The problem is that when one uses gem2rpm,
`~>` is expanded to `>=` and `<=`, which leads to list some dependencies twice.

![Double dependencies]({filename}/images/fedoraruby_duplicate_entries.png)

The fix was quite easy. Here is the controller that is in charge for the show
action:

```ruby
  def show
    @name = params[:id]
    @rpm = FedoraRpm.find_by_name! @name
    @page_title = @rpm.name
    @dependencies = @rpm.dependency_packages.uniq
    @dependents = @rpm.dependent_packages.uniq
    rescue ActiveRecord::RecordNotFound
      redirect_to action: 'not_found'
  end
```

All I did was to add `uniq`.

### duplicate homepage and source uri

In a gem page you could see this:

![Double homepage]({filename}/images/fedoraruby_duplicate_homepage_gem.png)

The information is taken from the <https://rubygems.org> api. Some have the
same page for both gem's homepage and source uri. The secret was lying in the
[view][].

```ruby
%div.info
  %h3 Gem Information
  %p
    Homepage:
    =link_to @gem.homepage, @gem.homepage
  - unless @gem.source_uri.blank?
    %p
      Source Code:
      =link_to @gem.source_uri, @gem.source_uri
```

All I did was to change this from this:

```ruby
- unless @gem.source_uri.blank?
```

to this:

```ruby
- unless @gem.source_uri.blank? || @gem.source_uri == @gem.homepage
```

So now it skips showing the homepage if it is the same as the source uri.

## Enhancements

### Show more info in fedorarpm show page

I added some more information at the fedorarpm page. Now it shows, last packager,
last commit message and last commit date. Useful if something is broken with
the latest release and you want to blame someone :p

And since many times a package has many co-maintainers you get to see the real
last packager.

Here's a shot of the page as it is now:

![More info]({filename}/images/fedoraruby_moreinfo.png)

### Rake tasks

As I have made some [major refactoring][pr] in the fedorarpms model, I split
many methods to their own namespace. For example, previously there was a single
method for importing the versions and dependencies, now they are two separate.

As a consequense, I added rake tasks that could be invoked for a single package.
Also the namespace is now more descriptive.

The tasks are for now the following:

```
rake fedora:gem:import:all_names               # FEDORA | Import a list of names of ALL gems from rubygems.org
rake fedora:gem:import:metadata[number,delay]  # FEDORA | Import gems metadata from rubygems.org
rake fedora:gem:update:gems[age]               # FEDORA | Update gems metadata from rubygems.org
rake fedora:rawhide:create                     # FEDORA | Create file containing Fedora rawhide(development) version
rake fedora:rawhide:version                    # FEDORA | Get Fedora rawhide(development) version
rake fedora:rpm:import:all[number,delay]       # FEDORA | Import ALL rpm metadata (time consuming)
rake fedora:rpm:import:bugs[rpm_name]          # FEDORA | Import bugs of a given rubygem package
rake fedora:rpm:import:commits[rpm_name]       # FEDORA | Import commits of a given rubygem package
rake fedora:rpm:import:deps[rpm_name]          # FEDORA | Import dependencies of a given rubygem package
rake fedora:rpm:import:gem[rpm_name]           # FEDORA | Import respective gem of a given rubygem package
rake fedora:rpm:import:koji_builds[rpm_name]   # FEDORA | Import koji builds of a given rubygem package
rake fedora:rpm:import:names                   # FEDORA | Import a list of names of all rubygems from apps.fedoraproject.org
rake fedora:rpm:import:versions[rpm_name]      # FEDORA | Import versions of a given rubygem package
rake fedora:rpm:update:oldest_rpms[number]     # FEDORA | Update oldest <n> rpms
rake fedora:rpm:update:rpms[age]               # FEDORA | Update rpms metadata
```

That was it for now. For any changes be sure to check out the changelog regularly!

[pr]: https://github.com/axilleas/isitfedoraruby/pull/54
[gitweb]: http://pkgs.fedoraproject.org/cgit
[stats]: https://github.com/axilleas/isitfedoraruby/graphs/contributors
[pkgwat]: https://github.com/daviddavis/pkgwat
[vcr]: https://github.com/vcr/vcr
[webmock]: https://github.com/bblimke/webmock
