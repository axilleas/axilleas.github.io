Title: GitLab repository management book review
Tags: gitlab, book, review
Category: reviews

I remember when I was trying to install GitLab 2.0 with no prior knowledge 
of the rails framework and ruby in general, just copy pasting commands. It seemed fun
and when the login screen showed for the first time, it felt really great!
And then I remember searching for the default username/password. It wasn't documented,
rather than shown somewhere between the commands I was blindly copying. Since then 
a lot has changed, the documentation got a lot better, the community has grown big and 
GitLab took the way it deserved. In my last post I wrote that I would review the new book that [Jonathan M. Hethey][twitter] wrote about GitLab. Without further ado, let's have a look what this book offers, what not and what I would like to see included in its next version.

![GitLab Repository Management](http://www.packtpub.com/sites/default/files/1794OS.jpg)

[TOC]

## Chapters

### Kickstarting with GitLab

The first chapter describes the features of GitLab, points to the cloud-based solution offered by GitLab.com and refers to its competitors (open source or closed source).
If you have never heard about GitLab before, this will get you started.

### Installation

As you'd have guessed, the installation guide is there to follow, sticking as possible  to the original one written by the GitLab devs. Unfortunately for the readers, since GitLab is evolving rapidly, it is only common for this chapter not to be completely up to date with the one upstream provides. My advice is, if you decide to install GitLab, you should follow the official guide and consult this book to better understand what ecah command does.

### Configuring GitLab

Again, the configuration steps come mainly from the installation guide but are more coprehensive and better explained so you'll get a good understanding why you do what you do. You will be also introduced to the ssh protocol and learn how you can add more protection to your the server by changing the default port sshd listens to, as well as how to configure this to play well with GitLab. If you are new to the UNIX world and were blindly typing commands before, this chapter will help you grasp the reasoning behind each command. 

### Roles and permissions

As stated in the book, where GitLab excels is its intuitive web UI tied with Git and the different management user roles it provides. In this book you will learn in depth about this feature. Every role is explained extensively, with examples where possible. Also you will learn how to log in for the first time, how to create your personal ssh key, how to add new users manually through the administrative interface and how to enable sign up.

### Issues and wiki

One other aspect of GitLab that makes it ideal for collaborating is its embedded issue  tracker and the wiki it provides. Being part of a team, you will want to make code reviews, exchange ideas and document your software. The "Issues and wiki" chapter will help you grasp those ideas and also learn some "hidden" functionalities like the ability to refer to other elements inside GitLab through shortcodes (issues, Merge Requests, snippets, milestones, commit messages, etc.). Beware that there is some extensive reference to teams, a feature deprecated in newer versions and superseded by groups.

### Workflows

In the sixth chapter you are introduced to the GitLab workflow, which if you have ever used Github, you have a pretty solid ground of understanding how it works. As I mentioned earlier, GitLab is primarily used for code review among developers and the workflow of feature branches works very well with the web UI GitLab provides, where you can create merge requests and fork projects to your own namespace. If you are not familiar with the merge request term, you will learn all about it through this chapter. The idea of Git hooks is also introduced and an example is provided for better understanding. Unfortunately there is no reference to web hooks, a feature that lacks documentation and used by many users. I would really like to see a section about web hooks in a future edition of this book.

### Updating GitLab

Since GitLab is a rapid developed project and a new version comes out each month, you will need to know how to update it. The 3-step golden rule, backup, backup and backup applies here as well, particularly if you are an administrator dealing with a corporate environment with many projects and users. In the "Updating GitLab" chapter you are presented with some common backup options like `tar` and `mysqldump`, and you will learn how to first ensure a proper backup is taken and then update you GitLab Installation. As the author states, when updating you should always watch out for the current update guides available at the official repository. A nice chapter overall that learns you the importance of, what else, backup.

### Help and Community

In the last chapter you will learn the various channels where you can get help. Basically it's a somewhat more detailed version of the [Getting Help][gethelp] section of the README file.

## To sum up

Overall, this book is a great starting point for newcomers to the GitLab world that have little or no prior knowledge of the git workflow. For administrators that want to install and use GitLab in their organization, it's also a good starting point and a detailed reference for the main functionalities GitLab provides.

Given its daily development, sections as "Installation" and "Update" should not be taken literally, as the upstream guides are more accurate and up to date.

Personally, I expected it to have more information for administrators that already know their way in using the interface. Things like

- ldap configuration
- setup of other omniauth providers
- usage of webhooks
- communicating with the api

are some of the advanced functionalities I would like to have seen. Hopefully in a newer version these will be provided. 

If I were to grade this book I would give it a 7/10. Not at all bad, but not exceeding my expectations. I hope Jonathan will take these considerations into account and update the book sometime soon :) In the meantime go grab yourself a [copy][book]!


[twitter]: https://twitter.com/JonathanMH_com
[gethelp]: https://github.com/gitlabhq/gitlabhq/blob/master/README.md#getting-help
[book]: http://bit.ly/1fTUYMy