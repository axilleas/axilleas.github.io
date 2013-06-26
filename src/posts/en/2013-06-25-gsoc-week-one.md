Title: GSoC - Weekly update 1
Tags: gsoc, fedora
Category: geek

It's been over a week that GSoC started and here is a weekly report of what achieved
so far.

## Weekly process

### Workflow
[Trello board][] - This is a web app in which you can manage your workflow by adding
tasks that are to be completed. I set it up to remind me the things I have to accomplish
in due time. Cool thing is that there is an android app too, so I can manage it
from wherever I am :)

### First package
I submitted my first package to Bugzilla for review. Yay! It is called [timers][]
and is of course a rubygem (what else :p). Not a big deal, just an easy one to get
me started.

### List of gems to package
I re-calculated GitLab's gem dependencies, this time including only the ones
needed for runtime. I ditched from the list the ones that are used for testing/development.
Not that they are not useful, but for the time being runtime dependencies
are a priority. I used a really ugly hack but it works for now. Here is how:
Clone [GitLab][], cd into it and run:
  
    ::bash
    bundle exec install --deployment --without test development

This will install all deps included in the Gemfile except for the ones in test and 
development groups. Then, using a for loop we can iterate under the `vendor/bundle/ruby/1.9.1/gems`
directory and write the results in a file.

  
    ::bash
    for i in `ls vendor/bundle/ruby/1.9.1/gems`; do echo $i >> ../gitlab53-gems; done


The list contains gems in the format of `gem_name-1.0.0` so I had to clean that
up a little. I used some string methods in the [python script] and stored those values
in a dictionary where key is the gem name and value its version. Then the names
list was easily retrievable. All I had to do is call the `keys()` method on
the dictionary and store the result in a [file][gitlab53-gems].

Then, I had somehow to include in the list of already packaged gems, the ones that 
are submitted in bugzilla for review. No need to work on them if their specfile
is already submitted for review, right? For that I used the [python-bugzilla][pb]
tool that queries a Bugzilla instance and spits nice [formated results][bz-query].
The query is pretty much self explanatory. In the end I just sorted them according
to their bug status.

    ::bash
    bugzilla query --product=fedora --bug_status=new,assigned --component='Package Review' \
    --short_desc='rubygem-' | sort -k2 -r > $bugzilla_gems_raw

Below, using the same query methods and some sed/awk magic[^json], we end up with a file
containing only the names of gems that are submitted for review in Bugzilla.

    ::bash
    bugzilla query --product=fedora --bug_status=new,assigned --component='Package Review' \
    --short_desc='rubygem-' | awk 'BEGIN { FS = " - " }; { print $3 }' | awk 'BEGIN { FS = ":" }; { print $2 }' \
    | sed -e 's/rubygem-//' | sort -k1 > $bugzilla_gems

That list, combined with the query from the official repos, results in the [final][]
one which has all the Ruby gems already packaged or are to be packaged for Fedora.

I also wrote a method to store those values in a [dictionary][bz-dict] in the format
of `dict = { gem_name: [bug_id, status, assignee, description] }`. It might come
in handy in the future, who knows!

Next step was to find the missing gems that I will have to package for Fedora.
Comparing those two lists we end up with this [list][missing-gems].

And the new results are:

  > Gitlab uses **143** runtime gems.
  >
  > Fedora has packaged **461** gems.
  >
  > There are **73** common gems.
  >
  > There should be packaged **70** gems.
  >
  > Fedora will have **15.18 %** more ruby packages, that is **531** gems in total.


### Gem tree dependencies
There are a lot of gems that depend on each other which means one has to
be picky as to what to package first. The best way would be: given a package,
find its dependency tree and start packaging first the leafs that have no children
going all the way up until you reach to the root.

I started writing a [script][gemtree] in ruby as a way to better learn the language,
but I have yet to iplement the DFS algorithm which will traverse through all
dependencies. Any comments on how to best approach this are welcomed!

***Update!!*** I just found out this reaaally cool site: [https://gemlou.pe][]
which parses rubygems.org and lists the runtime tree dependencies of a gem through 
javascript!

### Article about gem packaging
I started writing an article about packaging a Ruby gem in Fedora. I want to
note down the whole process, beginning from the use of gem2rpm to the review process.
At first I wanted to have it finished by this week, but the information is so vast
that I will take my time and write it piece by piece. You can follow the process [here][draft].

## TODO

Some TODOs for this week:

- Continue writing the article about Rubygem packaging
- Make some unofficial package reviews in order to get [sponsored][] as a packager
- Make more package submissions (I have some specfiles ready)
- Start wikifying the process (like the [Gitorious][] page)

## Extras

Apart from the GSoC program that is an awesome experience, there are some other
cool stuff going on this summer. 

First one is [Euruko][] which will take place in
Athens, so it will be easy to attend. I have already purchased a ticket. I am sure
that it's gonna be awesome and I'll get to meet the GitLab devs as well :)

The other one is a MOOC by UC Berkley and is a course about agile development and SaaS.
It has two parts:

  - [CS169.1x][] starts on July 2nd and is lasting 5 weeks
  - [CS169.2x][] starts on August 13th and is lasting 6 weeks

The language they use is Ruby and the framework on which they build the apps is
Rails. I am going to attend both courses as it is strictly related to GitLab and
my GSoC involvement. Actually, I already bought the accompanying [book][] (not mandatory)
and started reading it :)

I will try to be more on schedule next time and post about my progress at the end
of each week.

Cheers!

[^json]: It would make matters easier if the query returned a json file. I haven't
seen anything in the man page about json support.

[Trello board]: https://trello.com/board/gitlab/51b844202ed21a6735011b25
[timers]: https://bugzilla.redhat.com/show_bug.cgi?id=969877
[GitLab]: https://github.com/gitlabhq/gitlabhq
[python script]: https://github.com/axilleas/fedora/blob/master/gitlab-deps/gemfile.py#L30
[gitlab53-gems]: https://github.com/axilleas/fedora/blob/master/gitlab-deps/rubygems_gitlab
[pb]: https://fedorahosted.org/python-bugzilla/
[bz-query]: https://github.com/axilleas/fedora/blob/master/gitlab-deps/rubygems_bugzilla_raw
[final]: https://github.com/axilleas/fedora/blob/master/gitlab-deps/rubygems_fedora
[bz-dict]: https://github.com/axilleas/fedora/blob/master/gitlab-deps/gemfile.py#L95
[missing-gems]: https://github.com/axilleas/fedora/blob/master/gitlab-deps/rubygems_missing
[gemtree]: https://github.com/axilleas/fedora/tree/master/gitlab-deps/gemtree
[Gitorious]: https://fedoraproject.org/wiki/User:Ktdreyer/Gitorious
[sponsored]: https://fedoraproject.org/wiki/Join_the_package_collection_maintainers#Get_Sponsored
[Euruko]: http://euruko2013.org/
[CS169.1x]: https://www.edx.org/course/uc-berkeley/cs-169-1x/software-service/993
[CS169.2x]: https://www.edx.org/course/uc-berkeley/cs-169-2x/software-service/1005
[book]: http://www.saasbook.info/
[https://gemlou.pe]: https://gemlou.pe
[draft]: https://github.com/axilleas/axilleas.github.io/blob/source/src/posts/en/2013-06-12-fedora-rubygem-packaging.md
