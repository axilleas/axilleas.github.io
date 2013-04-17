Title: Bringing GitLab to Fedora
Slug: bringing-gitlab-in-fedora
Tags: fedora, gitlab, gscoc, ruby, rails
Category: linux
Lang: en

So, I decided to write some info regarding my involvement for this year's
[Google Summer of Code][gsoc]. I have been using/testing GitLab since
version 2.0 (almost a year now) and I am thrilled to see how much it has
growed since. This year I got a little more involved into this and
I made [two][commit-docs] [commits][commit-code] upstream. Nothing fancy, but I hope to
contribute more as time passes by.


In the rest of this article I will try to explain what GitLab is,
how Fedora is involved into all this and what are the benefits of this involvement.
This is the first of many follow-up posts I intend to write, so keep tight!


[TOC]

# What is GitLab?

[GitLab][gl-site] is an [open source][gl-github] MIT licenced [git] repository
management application. It is built on [Ruby on Rails][rails] and is
one of the most [popular][github-popular] projects featured on Github.
It is used by many companies as their internal git management repository.
The reason it gained so much popularity is that it bares a strong resemblance
to github's [looks][gl-screenshots] and [feels][gl-features].
It is a project with great potential, under heavy development with a release
cycle every month. That makes it possible to apply bug fixes quite regularly
and test new features. And since a picture is worth a thousand words, here is
a [demo site][gl-demosite] where you can test all the latest features.


# Fedora's involvement so far

The thought of GitLab being packaged and deployed for [Fedora Hosted] isn't new.
It all started last March when [Dan Allen][] [proposed][gl-proposal2012] GitLab 
to be used as a service for Fedora Hosted. If you follow the conversation 
it summarizes to some key points:

  - Projects pages should be ideally hosted as `$projectname.fedorahosted.org`.
  - GitLab and its dependencies should be packaged for Fedora and EPEL 6.
  - Puppetize the whole thing up. [There][gl-puppet1] are [some][gl-puppet2] configs, but they'll sure need some adjustment.
  - We need to form a team of maintainers for longterm support even after GSoC is over.

There was even a [post][fedora-glgroup] in GitLab's list, also by Dan Allen,
bringing the project to the attention of the GitLab community.
The most interesting thing was that the [lead developer][randx] of GitLab 
was more than willing to help. In the end, there was an [application][gl-gsoc12] but 
unfortunately that was the last anyone heard about the project.

So, here we are a year after with me applying for the project. To be exact
there is [another][harish-fellow] sudent interested in this as well, so that makes it two of us.
I have already expressed my interest in [RubySIG][] and in the [infrastructure][] mailing list.
I was glad to see that there was a positive response from Dan Allen,
as well as some valuable advice from user [Ken Dreyer][] who currently 
tries to deal with [Gitorious][].

# What are the benefits

There are two major benefits for Fedora.

## Get more ruby packages in the repos

Prior to addressing my interest in the mailing lists, I approached [Vít Ondruch][] to get some feedback about this task.
He was very helpful and pointed me to what should be done as a first step.
That is

  1. identify which gems are missing in Fedora and package them,
  2. compile a list of gems GitLab is using, including all their dependencies (and possibly bundled dependencies).
 

For the first task, I used a hackish bash script which first accumulates 
all rubygems in a file and then removes the duplicate packages and the ones
that are documentation.
    
    ::bash
    #!/bin/bash

    file_raw='/home/axil/tools/fedora-gitlab/rubygems_fedora_raw'
    file_new='/home/axil/tools/fedora-gitlab/rubygems_fedora'

    yum search all rubygem | awk '{print $1}' > $file_raw

    sed -e 's/rubygem-//g' -e 's/.noarch//g' -e 's/.x86_64//g' \
    -e '/i686/d' -e '/==/d' -e '/:/d' -e '/-doc/d' < $file_raw > $file_new


In order to find what gems GitLab depends on, I used the [Gemfile.lock][] 
and wrote a simple python [script][gemfile.py][^python-script] that computes how many and which gems 
Fedora and GitLab have in common. Below are some draft[^draft_numbers] numbers and a bar chart.

<div id="rubygems_chart"></div>

  > Gitlab uses: **203** gems.
  >
  > Fedora has packaged: **385** gems.
  >
  > There are **97** common gems.
  >
  > There should be packaged: **106** gems.
  >
  > Fedora will have **27.53 %** more ruby packages, that is **482** gems in total.




Not bad, **106** more ruby packages! That is a plus now that Fedora is considered 
one of [Ruby's supported platforms][ruby-supported]. 

**Update:** I just found out about the [gemfile tool][] that isitfedoraruby.com[^isitfedruby]
is using. This will come in handy. 

## A new service for fedorahosted.org

After the packaging is done, the next big thing is the deployment process on 
[Fedora Hosted][] as a new service. Quoting Dan Allen's [thought][deploy-quote]: 

  >One of the key reasons I've been pushing for GitLab is because I see the
  >potential it has for drastically improving the discoverability of the
  >Fedora code base and encourage participation. I've been involved with a lot
  >of projects on GitHub and I'm amazed by how simple it is to submit changes
  >(to both code and documentation). In fact, it's often easier to send a
  >patch with a description of the change than to create an issue...flipping
  >the normal bug submitting process on its head.
  >
  >GitHub also works because it enables collaboration over coordination. You
  >don't have to ask for permission on GitHub. You just do it. Then you can
  >easily track when they get pulled in or changes are requested. (the same is
  >true of GitLab).
  >
  >With GitLab, we can bring that experience to the Fedora community. It's a
  >large enough community (esp in terms of repositories), that I'm positive
  >we'd see that collaboration kindle within the Fedora instance.

So yeah, this is a big deal from this point of view :)

# Next steps and things to overcome

There is certainly a lot more to do. For starters, as a Fedora newbie, 
I have to run through the [Ruby guidelines][ruby-guidelines] and learn 
about the philosophy of rpm. Luckily, I am not a linux newbie (I've been 
using Archlinux for 5 years) and I am adopting rapidly.
Then, I need to learn some Ruby. I have already printed *[why's (poignant) Guide to Ruby][poignant]*
which is considered a must read, and believe me it is! (download the pdf from [here][poignant-pdf]). 
[Learn Ruby the hard way][hardway] is also a good starting point. Ι think I'm on the right track.

Now, as far as the packaging process is concerned, here is what more needs to be done:
 
  - MariaDB support. Since MariaDB will be the [default][mariadb-list] [implementation][mariadb-wiki] of MySQL in Fedora 19, GitLab will need to support it.
  - Write systemd service files. I had made an [attempt][gh-systemd] two months ago when I was trying to set up GitLab on Archlinux, but it is far from perfect.
  - Packages to be EPEL compatible. A great advantage if GitLab gets packaged for Fedora, is that it would make it as easy as pie to install on a server running Red Hat, Centos, or some other rpm based distro.
  - Ruby 2.0 compatibility. I don't think that'll be much of a stopper since GitLab is in the [process][gl-ruby2] of supporting it, but I put it here just in case.
 
That's all for now. If you read through here you should have a good understanding
of this project's goal. More posts to come!
 
 
[^python-script]: I should write it in ruby, I know :p
[^draft_numbers]: I say draft, mainly because that is a raw calculation of GitLab's dependencies. One has to take into account the different/old versions that may exist between Fedora and GtiLab. There are also some packages GitLab pulls from git and not rubygems.org. 
[^isitfedruby]: [isitfedoraruby.com][] is a cool web app that was the result of [last year's GSoC][gsoc12].

[gl-gsoc12]: https://fedoraproject.org/wiki/GSOC_2012/Student_Application_babakb/GitlabSetup "Student application for GitLab at GSoC 2012"
[gsoc12]: https://fedoraproject.org/wiki/GSOC_2012/Student_Application_Zuhao/IsItFedoraRuby
[isitfedoraruby.com]: http://isitfedoraruby.com
[gl-ruby2]: https://github.com/gitlabhq/gitlabhq/commit/52cd655f71c6a5393b71640c13cd95e35e8d2624
[gemfile tool]: http://isitfedoraruby.com/stats/gemfile_tool
[gh-systemd]: https://github.com/axilleas/gitlab-recipes/tree/master/systemd
[poignant-pdf]: https://github.com/downloads/mislav/poignant-guide/whys-poignant-guide-to-ruby.pdf
[poignant]: http://mislav.uniqpath.com/poignant-guide
[hardway]: http://ruby.learncodethehardway.org/book/
[ruby-guidelines]: https://fedoraproject.org/wiki/Packaging:Ruby
[mariadb-list]: https://lists.fedoraproject.org/pipermail/devel/2013-January/176584.html "Proposed F19 Feature: Replace MySQL with MariaDB"
[mariadb-wiki]: https://fedoraproject.org/wiki/Features/ReplaceMySQLwithMariaDB "Features/ReplaceMySQLwithMariaDB"
[gem2rpm]: https://github.com/lutter/gem2rpm "convert ruby gems to rpms"
[deploy-quote]: https://lists.fedoraproject.org/pipermail/infrastructure/2013-March/012680.html
[ruby-supported]: https://bugs.ruby-lang.org/projects/ruby-trunk/wiki/20SupportedPlatforms
[gemfile.py]: https://github.com/axilleas/fedora-gitlab/blob/master/gemfile.py
[Gemfile.lock]: https://github.com/gitlabhq/gitlabhq/blob/master/Gemfile.lock
[Vít Ondruch]: https://fedoraproject.org/wiki/User:Vondruch
[gsoc]: http://www.google-melange.com/gsoc/homepage/google/gsoc2013 "Google Summer of Code 2013"
[gl-site]: http://blog.gitlab.com "GitLab home page"
[git]: http://git-scm.com "git home page"
[rails]: http://rubyonrails.org/ "Ruby on Rails"
[github-popular]: https://github.com/popular/starred "GitLab featured in Github's most popular repos"
[gl-demosite]: http://demo.gitlab.com/users/sign_in "GitLab demo site"
[gl-features]: http://blog.gitlab.com/features/ "GitLab features"
[gl-screenshots]: http://gitlab.org/screenshots/ "GitLab screenshots"
[gl-github]: https://github.com/gitlabhq/gitlabhq "GitLab on Github :p"
[commit-docs]: https://github.com/gitlabhq/gitlabhq/commits/master/doc/install/installation.md?author=axilleas
[commit-code]: https://github.com/gitlabhq/gitlabhq/commits/master/lib/tasks/gitlab/check.rake?author=axilleas
[Dan Allen]: https://fedoraproject.org/wiki/User:Mojavelinux
[gl-proposal2012]: https://lists.fedoraproject.org/pipermail/infrastructure/2012-March/011463.html
[Fedora Hosted]: http://fedorahosted.org
[gl-puppet1]: https://forge.puppetlabs.com/sbadia/gitlab
[gl-puppet2]: https://forge.puppetlabs.com/lboynton/gitlab
[fedora-glgroup]: https://groups.google.com/forum/?fromgroups=#!topic/gitlabhq/SQMDi-yyXmU
[randx]: https://github.com/randx
[harish-fellow]: https://lists.fedoraproject.org/pipermail/summer-coding/2013-March/000286.html
[RubySIG]: https://lists.fedoraproject.org/pipermail/ruby-sig/2013-March/001270.html
[infrastructure]: https://lists.fedoraproject.org/pipermail/infrastructure/2013-March/012631.html
[Ken Dreyer]: https://fedoraproject.org/wiki/User:Ktdreyer
[Gitorious]: https://fedoraproject.org/wiki/User:Ktdreyer/Gitorious

<!--Load the AJAX API-->
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">

  // Load the Visualization API and the piechart package.
  google.load('visualization', '1.0', {'packages':['corechart']});

  // Set a callback to run when the Google Visualization API is loaded.
  google.setOnLoadCallback(drawChart);

  // Callback that creates and populates a data table,  
  // instantiates the pie chart, passes in the data and
  // draws it.
  function drawChart() {

  // Create the data table.
  var data = new google.visualization.DataTable();
  data.addColumn('string', '');
  data.addColumn('number', 'rubygems');
  data.addRows([
    ['GitLab', 203],
    ['Fedora', 385],
    ['Common', 97],
    ['To be packaged', 106],
    ['Total after packaging', 482]
    ]);

  // Set chart options
  var options = {'title':'Numbers calculated on 08-04-2013', 'width':600, 'height':500};

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.BarChart(document.getElementById('rubygems_chart'));
  chart.draw(data, options);
  }
</script>
