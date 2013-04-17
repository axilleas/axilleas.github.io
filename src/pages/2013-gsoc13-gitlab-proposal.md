Title: GSoC 2013: Idea to setup GitLab as a frontend to fedorahosted.org (again!)
Slug: gsoc13-gitlab-proposal
Status: draft

Hello GitLab devs and community!

Last year, Dan Allen started a discussion [0] expressing Fedora's interest 
to deploy GitLab as a git frontend to http://fedorahosted.org. Unfortunately
the project didn't get picked up, so I am applying for this year's gsoc
in hopes of seeing it happen :) In fact, there are also two[1] other[2] 
students interested in this as well, so this is definately going somewhere!
I made a blog post [3] where I describe the story so far and the benefits 
for Fedora. What I would like to express in this post, are the possible 
benefits for GitLab as well. 

- Fedora is one of the bigest open source communities (if not the bigest)
so far, with a very strong community base. If GitLab were to be supported
officially, it would gain much more reputation and probably  set up as the de facto
git management system for other orgs that want control over their personal 
git repositories.

- rpm packages means "One click install" for Fedora, Red Hat, Centos and other
rpm based distros. Huge profit, as sysadmins will not have to worry about
the manual installation process.

- As an extra git service for fedorahosted.org, I expect many people to switch
their git hosting from the bare gitweb to GitLab. It will enhance collaboration
and make coding more fun as it will be an interactive process.


Showstoppers

At this moment, Fedora's infra team [4] is reluctant [5] on having GitLab as 
a git service, due to the fact that it doesn't support public browserability. 
I know this has been discussed several times in the past and GitLab devs
have expressed their non interest in making this happen, but I have to ask.
Are you at least _considering_ the possibility that this long awaited [6][7] 
feature will get implemented some time in the near future? I don't mean
to put any pressure, but IF this is considered to happen, a roadmap would
be perfect as this project probably won't make it to Fedora otherwise.

Thank you for taking the time to read this and I am looking forward to any
feedback :)

Cheers!

Axilleas


[0] https://groups.google.com/forum/?fromgroups=#!topic/gitlabhq/SQMDi-yyXmU

[1] https://lists.fedoraproject.org/pipermail/summer-coding/2013-March/000286.html

[2] https://lists.fedoraproject.org/pipermail/infrastructure/2013-April/012758.html

[3] http://axilleas.github.io/en/blog/2013/bringing-gitlab-in-fedora

[4] https://fedoraproject.org/wiki/Infrastructure

[5] https://lists.fedoraproject.org/pipermail/infrastructure/2013-April/012764.html

[6] http://feedback.gitlab.com/forums/176466-general/suggestions/3159951-allow-public-repositories

[7] http://feedback.gitlab.com/forums/176466-general/suggestions/3776706-allow-internal-open-public-repositories
