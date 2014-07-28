Title: Custom GitLab login page
Slug: custom-gitlab-login-page
Tags: ruby, rails, webdev, gitlab, haml
Category: geek
Lang: en

With the [release of GitLab 7.1][rel71], the login page now looks like the
default Enterprise Edition. Although in EE customizing the page should be
easier to configure, we can do the same with Community Edition following
some simple steps. If you are familiar with [haml][] and [bootstrap][]
this should be fairly easy for you. Again, prerequisite is to have at least
GitLab 7.1. You can see the final changes in this [commit][].

Here is a before/after screenshot that we will gradually change.

![Before](|filename|/images/gitlab_custom_login_before.png)

![After](|filename|/images/gitlab_custom_login_after.png)

[TOC]

## Introductory steps

### haml identation

It is important to use an editor that has set a tab to two spaces.
Haml depends on indentation so any mistake will yield errors. If you see
any 500 errors, it means something went wrong. Either check the unicorn logs
or better, run `git diff` to see if there are any indentation errors.

If you are using vim, create/open `/home/git/.vimrc` and place the following
lines:

```
set tabstop=2
set shiftwidth=2
set expandtab
```

That will ensure proper indentation handling.

### git branch

In order to have more seamless future updates, let's create a separate git
branch:

```bash
su - git
cd /home/git/gitlab/
git checkout -b custom_login_page
```

All changes we make from now on, will be on that branch without creating
any mess in future updates. Read below on how to update.

---

The main file we need to change is `app/views/layouts/devise.html.haml`,
relative to where GitLab is installed.

## Change brand logo

Choose the image you want to appear in the login page and place it in
`/home/git/gitlab/app/assets/images/`.

Next, open `app/views/layouts/devise.html.haml` with an editor and change
[line 22][ln22] replacing `brand_logo.png` with your image name including
its extension.

Since we alter the production server, remember to recompile the assets so
that the [Rails asset pipeline][assets] picks the new image (do that every
time you put a new file or change something in `app/assets/`):

```bash
cd /home/git/gitlab/
sudo -u git RAILS_ENV=production bundle exec rake assets:precompile
```

Finally, restart the GitLab service to see the changes.

## Change text

Apart from the logo, there is a lot more we can change. Let's try changing
the text.

### Brand title

In order to change the text reading *GitLab Community Edition*, open
`devise.html.haml` and change `%h1= brand_title` in line 9 into
`%h1 My custom brand title`. Here, we removed the equal sign because it
is used by haml to evaluate and print ruby code (`brand_title` is a helper
method).

If you want an image instead, you can replace `%h1= brand_title` with
`= image_tag 'my_banner.png'`.

### Body description

As you'd imagine, changing the body headline would require to replace
`%h2 Open source software to collaborate on code` with our own text, or
even remove it completely.

The main body can be changed by altering the text that lies below `%p.lead`.
Remember to indent correctly.

The text can also contain links. Place each link in its own line.

An example would be:

```
Accounts are temporarily created manually, you can ask one in our
= link_to "forum discussion", "https://forum.example.com/gitlab-reg"
You can find more info in the
= link_to "Wiki.", "https://example.com/wiki/index.php/GitLab"
```

A link can also have a `target = "_blank"` to open in a new window.
The [format][] is:

```
= link_to "text", "http://example.com", target: "blank"
```

## Change footer links

Footer links are in [line 35][ln35]. Just change their content or add new
ones like we talked above.

## Change font

The text I used was in Greek, so it looked aweful since the default font
is *Helvetica Neue*. I decided to change it and use a webfont that supports
my language. I went with *Open Sans* from <https://www.google.com/fonts>.

Now, there are 3 changes we need to do:

1. Create our custom css file which imports the font and sets the classes
2. Change `devise.html.haml` and include the new css classes.
3. Include our custom css in `application.scss`.

For the first step I created `app/assets/stylesheets/custom_login.scss`
with contents:

```
@import url(http://fonts.googleapis.com/css?family=Open+Sans&subset=latin,greek);

.custom-login {
  h1, h2, p {
  font-family: 'Open Sans', sans-serif;
  }
}
```

Here I used [sass][]. These are nested values that will be picked by html.

The second step is to change `devise.html.haml` and include the new
`custom-login` css class. There were 2 places where I needed to do that:

```
- .brand_text.hidden-xs
+ .brand_text.hidden-xs.custom-login

- %p.lead
+ %p.lead.custom-login
```

Third step is to include the custom css in `application.scss`. I opened
`app/assets/stylesheets/application.scss` and appended at the very end of
the file the following:

```
/**
* Styles for custom login page
*/
@import "custom_login.scss";
```

Finally, in order for the new css to get included in the asset pipeline I
precompiled the assets one more time:

```bash
cd /home/git/gitlab/
sudo -u git RAILS_ENV=production bundle exec rake assets:precompile
```

And while I was trying to precompile the assets after adding my custom css,
it failed to do so because of a missing semicolon in `application.scss`.
I immediately opened a [Merge Request][mr], so either wait for it to get
merged or add it yourself for now. You got to love open source :)

Screenshots of before/after font change. You can see that before the changes
Greek and English words are using different fonts.

![Before font change](|filename|/images/gitlab_custom_login_prefont.png)

![After font change](|filename|/images/gitlab_custom_login_afterfont.png)

## Commit changes

The login page should now work correctly providing all the needed info for
our users. It's time to commit our changes. Check the diff with `git diff`
one more time, and make sure you are on the right branch with `git branch`.
It should show `* custom_login_page`. Add and commit the changed files:

```
git add app/
git commit -m 'Custom login page.'
```

## Updating GitLab

The trickiest part is to maintain the code through the updates and avoid as
many confilcts as possible.

Before each update, these are the basic steps:

1. Stop gitlab service
2. Run `git fetch --all`
3. Run `git branch 7-1-stable origin/7-1-stable` (replace with appropriate version)
4. Run `git rebase 7-1-stable custom_login`
5. Follow the rest of instructions (db:migrate, assets:precompile, etc.)

The trick here is rebase. This git command will replay our changes over the
new branch we fetched from upstream. If there are no conflicts, the custom
login changes will remain. Otherwise, git will inform you and then you'd
have to first resolve any issues before rebasing.

## Reverting changes

In order to revert to the original login page, it's as simple as changing
branches and restarting the GitLab service.

## What about omnibus?

If you have installed GitLab through the omnibus packages, the GitLab root
path will be `/opt/gitlab/embedded/service/gitlab-rails/` so make any
changes relative to that path. I haven't tested it yet though, so I don't
know whether any changes get rewritten with package updates (probably that
is the case).

On the other hand, if you work at a company that uses omnibus, consider
going for the Enterprise Edition where this process would be more easier
and at the same time you support the future development of GitLab :)


[rel71]: https://about.gitlab.com/2014/07/22/gitlab-7-dot-1-released/ 'Blog post: GitLab 7.1 released'
[assets]: http://guides.rubyonrails.org/asset_pipeline.html 'Rails asset pipeline'
[mr]: https://gitlab.com/gitlab-org/gitlab-ce/merge_requests/157
[sass]: http://sass-lang.com/guide
[ln22]: https://gitlab.com/gitlab-org/gitlab-ce/blob/master/app/views/layouts/devise.html.haml#L22
[format]: http://api.rubyonrails.org/classes/ActionView/Helpers/UrlHelper.html#method-i-link_to 'link_to definition'
[ln35]: https://gitlab.com/gitlab-org/gitlab-ce/blob/master/app/views/layouts/devise.html.haml#L35
[commit]: https://github.com/axilleas/gitlabhq/commit/953a8bc25f1cb5366026e6489c2716d0db69265c
[haml]: http://haml.info/docs/yardoc/file.REFERENCE.html 'haml yardoc files'
[bootstrap]: http://getbootstrap.com 'Bootstrap framework'