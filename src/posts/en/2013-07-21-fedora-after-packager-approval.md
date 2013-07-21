Title: I got approved as a packager, now what?
Tags: fedora, packaging, fedpkg, bodhi, git
Category: tech


This must have been the most intense week in terms of learning how the build 
system/process work in Fedora. I finally got approved as a packager and that means
more responsibility from my side. Unfortunately, the instrusctions in the wiki
are sometimes sparsed into different places and one has to read a lot and ask
around in order not to make any mistakes. For a newcomer all this information
is at least overwhelming and you have to even put a lot of thinking into asking
the right question in order to get the right answer.

I'm starting to believe that this is intentional as a continuous test to one's
understanding of how things work in Fedora. No pain no gain they say. 

Anyway, I kinda managed to understand most of it and below I will describe the
process I followed hoping to help any future-to-be packagers. I will describe the
whole process of my first package submission including the outputs of many commands
that were new to me. [This][sum-up] wiki page sums it up, but read it after understanding 
the process. There is also a nice guide called [packaging rpm workflow][] that shows
the workflow of the whole process from the very beginning. Nice read.

With the kind help of the people at `#fedora-devel` I was able to pull it through, 
so thanks guys :)

[TOC]

# Route to follow after your approval

Congratulations you promoted to a [packager][]! After your approval, there are a
bunch of things to do, summarized into two big steps:

1. Make a [scm request][] in your bugzilla review request
2. Use `fedpkg` to [commit, build and upload your package][add-to-scm]

Let's break it down.

## SCM request

Must read: [Package SCM admin requests][scm request]

For starters, scm stands for *Source Code Management*.
After your package approval, there are two steps as far as the Bugzilla concerns. 

1. set fedora-cvs flag to ?
2. Make a new comment including the following form completed:

        New Package SCM Request
        =======================
        Package Name: 
        Short Description: 
        Owners: 
        Branches: 
        InitialCC:

3. Hit `Save Changes` to save both 1 and 2. See [how][gem-bz] I did it.

**Note:** Let me tell you a little secret if you are new to bugzilla like I am. Make any
changes you need to, even leave a comment and then hit `Save Changes` to save ALL
the changes you've made. There are two buttons for this: one in the upper right
corner and one below the `Additional Comments` form. Either one will do just fine.
This may sound stupid but I wansn't aware of it, so I first left a comment and then
changed the flag, resulting to send a mail update twice.


## Commit, build and upload your package

Must read: [Add Package to Source Code Management (SCM) system and Set Owner][add-to-scm]

After the scm request, you will receive some e-mails from Bugzilla and PackageDB
stating that you are good to go. If you visit [cgit][] you will see your bare repository.

![Bare repo](|filename|/images/rubygem-bootstrap-sass.git-bare-2013-07-20-14-28-50.png)

The whole building process works using `fedpkg` and git commands, so if you are
not familiar with git, I suggest the [Fedora wiki page][git-fed]. For a more
comprehensive approach I highly recommend the [Pro Git book][progit].

### Steps with fedpkg and git

1. Create a directory to have all your package builds neat and tidy.

        ::bash
        mkdir ~/fedora-scm
        cd ~/fedora-scm

2. Clone the newly created git repository.

        ::bash
        fedpkg clone rubygem-bootstrap-sass
        cd rubygem-bootstrap-sass

    The contents of git config are:

        [core]
          repositoryformatversion = 0
          filemode = true
          bare = false
          logallrefupdates = true
        [remote "origin"]
          url = ssh://axilleas@pkgs.fedoraproject.org/rubygem-bootstrap-sass
          fetch = +refs/heads/*:refs/remotes/origin/*
        [branch "master"]
         remote = origin
         merge = refs/heads/master


3. Import the src.rpm:

        ::bash
        fedpkg import /var/lib/mock/fedora-rawhide-x86_64/results/rubygem-bootstrap-sass-f20.src.rpm
        
    You should see something like this:

        ::bash
        Uploading: 4f0c887ea7cd95812edcc6b8b01b9329  bootstrap-sass-2.3.2.1.gem
        ######################################################################## 100.0%
        Uploaded and added to .gitignore: bootstrap-sass-2.3.2.1.gem
        ...
        diff status of all files to be commited
        ...
        New content staged and new sources uploaded.
        Commit if happy or revert with: git reset --hard HEAD

    Now we have 3 files in our directory:

        -r--r--r--. 1 axil axil 86528 Jul 20 15:30 bootstrap-sass-2.3.2.1.gem
        -rw-r--r--. 1 axil axil  2314 Jul 20 15:30 rubygem-bootstrap-sass.spec
        -rw-r--r--. 1 axil axil    61 Jul 20 15:30 sources

    sources is a text file with the source package (gem) and its md5 hash.
    Notice that the gem name was automatically placed to the `.gitignore`.
    Running `git status` we see that there are 3 files in the [staging area][].

        # On branch master
        # Changes to be committed:
        #   (use "git reset HEAD <file>..." to unstage)
        #
        #       modified:   .gitignore
        #       new file:   rubygem-bootstrap-sass.spec
        #       modified:   sources
        #

    If you are indeed happy with the changes, commit them and push to master (rawhide) branch.
    Use the bugzilla id from your review request. No scripts are parsing this, it is just for reference.

        git commit -m "Initial import (#982679)."
        git push

    Now, if you visit again the cgit web page, you will see that the changes are submitted.

    ![Bare repo](|filename|/images/rubygem-bootstrap-sass.git-init-2013-07-20-15-58-58.png)

### Build on koji

Lastly, give this command to start a build on [koji][]:

    ::bash
    fedpkg build

Output:

    Building rubygem-bootstrap-sass-2.3.2.1-1.fc20 for rawhide
    Created task: 5631690
    Task info: http://koji.fedoraproject.org/koji/taskinfo?taskID=5631690
    Watching tasks (this may be safely interrupted)...
    5631690 build (rawhide, /rubygem-bootstrap-sass:md5): open (arm02-builder11.arm.fedoraproject.org)
    5631691 buildSRPMFromSCM (/rubygem-bootstrap-sass:md5): open (buildvm-25.phx2.fedoraproject.org)
    5631716 buildArch (rubygem-bootstrap-sass-2.3.2.1-1.fc20.src.rpm, noarch): open (buildvm-01.phx2.fedoraproject.org)
    5631691 buildSRPMFromSCM (/rubygem-bootstrap-sass:md5): open (buildvm-25.phx2.fedoraproject.org) -> closed
    0 free  2 open  1 done  0 failed
    5631716 buildArch (rubygem-bootstrap-sass-2.3.2.1-1.fc20.src.rpm, noarch): open (buildvm-01.phx2.fedoraproject.org) -> closed
    0 free  1 open  2 done  0 failed
    5631737 tagBuild (noarch): closed
    5631690 build (rawhide, /rubygem-bootstrap-sass:md5): open (arm02-builder11.arm.fedoraproject.org) -> closed
    0 free  0 open  4 done  0 failed

    5631690 build (rawhide, /rubygem-bootstrap-sass:054f742970e4b930bc55a5d3802fb31d26c57d0d) completed successfully

A notification mail will be sent to you once the build is complete and the
package will appear automagically at rawhide repos. If you want to push a
package to a stable version of Fedora, keep reading.

### Submit your package to current versions of Fedora

This step is optional if you want to maintain other versions than rawhide.
Switch to the corresponding version branch with `fx`, where `x` the version of Fedora:

    ::bash
    fedpkg switch-branch f19
        
Running `git branch -r` reveals our branches so far:

    ::bash
    origin/HEAD -> origin/master
    origin/f19
    origin/master

**Tip:** I suggest you use a shell where it shows you the branch you are in.
I recommend zsh and if you look at [oh-my-zsh][], almost all themes included
support this. Mine for example is: 

![My zsh theme](|filename|/images/zsh-git-branch.png)

Get the changes from master branch, push and build like before:

    ::bash
    git merge master
    git push
    fedpkg build

### Push your package to bodhi

If your local machine's username is the same as your FAS one, skip this step.
This option is hidden from the wiki guide, I spoted it [here][bodhi-user].

    ::bash
    echo "export BODHI_USER=axilleas >> ~/.zshrc"
    source ~/.zshrc

Replace `.zshrc` with your shell's rc.

The final step is to submit your package to bodhi in order to be processed and
reach the repositories. You have two options: either via terminal or via the webui 
of bodhi. Choose what fits you best.

If you prefer the webui method then go to [this link][bodhi-new], login and fill
in the blanks.

There are tooltips for each section explaining what should be filled,
but let's take a look:

| Description             |   Option                |                   Meaning                                                                     |
|:------------------------|:------------------------|:----------------------------------------------------------------------------------------------|
|Package                  | rubygem-bootstrap-sass  | Start typing your package name and it will autocomplete                                       |
|Type                     | newpackage              | Since this is the first package I chose newpackage                                            |
|Request                  | Testing                 | For the package to first land in updates-testing before goes in stable(recommended)           |
|Bugs                     | 982679                  | The bugzilla id of your review request. This way it will change its status automatically      |
|Notes                    | Package description     | Additional notes, eg. why you made this update, what are the bugfixes if it is a bugfix, etc. |
|Suggest Reboot           | untick                  | Recommend that the user restart their machines after they install this update                 |
|Enable karma             | tick                    | Enable update request automation based on [user feedback][karma]                              |
|Threshold to stable      | 3                       | This is the defaul value. It needs 3 points to get to stable repos                            |
|Threshold for unpushing  | -3                      | If it gets 3 points it rejects the package from testing                                       |


Your other option is to do the update through terminal. This only works with branches
other than rawhide. If you try to push to rawhide, `fedpkg` will warn you.

When you issue the command below, you will have to edit a template using the default
system editor which is `vi`. If you have a different preference eg. `vim`, use
the export command. While in `f19` branch:

    ::bash
    export EDITOR=vim
    fedpkg update
            
The template is this:
      
    [ rubygem-bootstrap-sass-2.3.2.1-1.fc19 ]

    # bugfix, security, enhancement, newpackage (required)
    type=

    # testing, stable
    request=testing

    # Bug numbers: 1234,9876
    bugs=

    # Description of your update
    notes=Here is where you give an explanation of your update.

    # Enable request automation based on the stable/unstable karma thresholds
    autokarma=True
    stable_karma=3
    unstable_karma=-3

    # Automatically close bugs when this marked as stable
    close_bugs=True

    # Suggest that users restart after update
    suggest_reboot=False

Once you make all the appropriate changes, save it and close it. You will be
asked your FAS password to complete the process and you will get a similar output:

    ================================================================================
         rubygem-bootstrap-sass-2.3.2.1-1.fc19
    ================================================================================
        Release: Fedora 19
         Status: pending
           Type: newpackage
          Karma: 0
           Bugs: 982679 - Review Request: rubygem-bootstrap-sass - Twitter's
               : Bootstrap, converted to Sass and ready to drop into
               : Rails or Compass
          Notes: Initial commit
      Submitter: axilleas
      Submitted: 2013-07-20 15:20:18

      https://admin.fedoraproject.org/updates/rubygem-bootstrap-sass-2.3.2.1-1.fc19


After the submission, your package will go through these [states][].

# FAQ

Here are some questions that I had during this process and their answers from
people in `#fedora-devel` which I thank them once again.

**Q:** During `fedpkg import src.rpm`, do I need to provide a `foo-f20.src.rpm` or `foo-f19.src.rpm` will work too?

**A:** You can virtually take any valid fedora/rhel srpm regardless on which version it was created.

**Q:** What if I accidentally run `fedpkg update` for rawhide (master branch)?

**A:** New versions of fedpkg should refuse.

**Q:** If in a package review the spec's release version was bumped, should I revert the release to 1 prior to pushing in cgit?

**A:** No, it is not needed.

# Epilogue

This was quite an adventure and I learned a lot. I am sure this is only the tip
of the iceberg and there's a lot more to come. This post took me literally one
day to compose as I was virtually recording the process as I performed it, hope
it was worth it. If you find any mistake or you want to add something please do
leave a comment. Next big article the Rubygem packaging How to ;)

Cheers!


[scm request]: https://fedoraproject.org/wiki/Package_SCM_admin_requests
[add-to-scm]: https://fedoraproject.org/wiki/Join_the_package_collection_maintainers#Add_Package_to_Source_Code_Management_.28SCM.29_system_and_Set_Owner
[sum-up]: https://fedoraproject.org/wiki/New_package_process_for_existing_contributors
[progit]: http://git-scm.com/book
[git-fed]: https://fedoraproject.org/wiki/Using_git_FAQ_for_package_maintainers
[bodhi-user]: https://fedoraproject.org/wiki/Package_update_HOWTO#Submit_your_update_to_Bodhi
[staging area]: http://git-scm.com/about/staging-area
[virgin]: http://koji.fedoraproject.org/koji/taskinfo?taskID=5631690
[oh-my-zsh]: https://github.com/robbyrussell/oh-my-zsh
[bodhi-new]: https://admin.fedoraproject.org/updates/new/
[first-review]: https://bugzilla.redhat.com/show_bug.cgi?id=969877
[packaging rpm workflow]: http://shakthimaan.com/downloads/glv/howtos/packaging-rpm-workflow.html
[gem-bz]: https://bugzilla.redhat.com/show_bug.cgi?id=982679
[koji]: https://fedoraproject.org/wiki/Koji
[cgit]: http://pkgs.fedoraproject.org/cgit/
[karma]: https://fedoraproject.org/wiki/QA:Update_feedback_guidelines
[states]: https://fedoraproject.org/wiki/Bodhi#Package_States
[packager]: https://fedoraproject.org/wiki/How_to_get_sponsored_into_the_packager_group
