Title: How to install Diaspora on CentOS 7
Slug: how-to-install-diaspora-on-centos-seven
Update: 2015-03-05 10:16
Tags: diaspora, centos, nginx, rails, ruby, fedoraplanet
Category: opensource
Lang: en

The tutorial isn't really hosted on my blog but on DigitalOcean's community
page, but I thought I could give some background regarding this decision.

## Introduction

Last November, me, [Nikos][] and [Pierros][] decided to run a [Diaspora][] pod to
accomodate the needs of the Greek community and also increase the number of
active pods around the world. Right now we have 662 registered users and the
number keeps growing :)

I had some experience in deploying Rails apps during my involvement with GitLab
and so I decided to share my findings in order that others could benefit as well.
This was also the first time I looked into Ansible so that we could easily
deploy our changes.

Our customizations are [free for everyone to see][librenetrepo] and so is our
[ansible code][ansiblerepo].

## Tutorial

Instead of publishing this on my blog, I decided to go bigger and contacted
Digital Ocean to see if they were interested in hosting an article on Diaspora
installation. After several weeks of email exchanging, testing and rearranging
bits of the tutorial, [it is finally live][article]!

Bare in mind that it is highly opinionated, based on the facts I gathered
during [librenet.gr][] deployment.

The reasoning behind this, is that DigitalOcean is viewed by way more people than
this little blog spot :p

Also it is no secret that DigitalOcean pays to write, so that way I can put
some money on server costs :)

### Bits to be careful about

After I posted the link to `#diaspora` on freenode, [jhass][], one of the core
contributors of Diaspora raised some concerns, so this post is also partially
trying to explain the desicions behind the steps I included in the tutorial.

First of all, do **NOT** run Diaspora on production with a self-signed certificate.
This will cause future problems, like your pod not being able to talk effectively
to other pods. I already sent my concerns to DO, so I expect it to change any
time soon.

Secondly, the guide relies on current stable version of Diaspora (`v0.4.1.2`)
and the article will be deprecated in many areas starting with version 0.5.
Among others, future versions of Diaspora:

* will create the database automatically with `rake db:create` asking for root
  password if it doesn't have permissions to create the DB
* will change the database collation from `utf8 -> utf8mb4`
* `ruby 2.0.0p353` which is in current CentOS repos, will be likely dropped
  in Diaspora 0.6 since it will be EOL'd in 2016

Also, the next version of Diaspora will have chat support which adds a whole
other level of complexity to set up.

Having said that, I will do my best to keep the current tutorial on par with
future Diaspora releases.


[Diaspora]: https://diasporafoundation.org/ "Diaspora foundation"
[Nikos]: http://www.roussos.cc/ "Nikos Roussos blog"
[Pierros]: http://pierros.papadeas.gr/ "Pierros Papadeas blog"
[article]: https://www.digitalocean.com/community/tutorials/how-to-run-an-open-source-distributed-social-network-with-diaspora-on-centos-7 "How To Run an Open-Source Distributed Social Network with Diaspora on CentOS 7"
[librenetrepo]: https://github.com/librenet/librenet.gr "librenet.gr on GitHub"
[ansiblerepo]: https://github.com/librenet/ansible "librenet.gr ansible repo"
[librenet.gr]: https://librenet.gr
[jhass]: http://jhass.eu/
