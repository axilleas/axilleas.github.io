Title: Rails development tools
Slug: ruby-on-rails-development-tools
Tags: fedora, gsoc, ruby, rails, webdev
Category: opensource
Lang: en

During the past two months I have been reading constantly about Rails and
how I could get more productive when writing code and testing my apps.
There is a ton of information about those matters on the web and I'll try
to include as many articles as I could find useful to my knowledge building.

*Disclaimer:* This article is heavily inspired by Thoughtbot's
[Vim for Rails Developers][] which I stumbled upon during browsing the
screencasts of [codeschool][].

[TOC]

# Editor of choice (vim)

When you work from the command line and you use linux, your editor
preference comes down to two choices: vim and emacs. I started with vim
some time ago so I'll stick with it.

If you are new to vim read this [cheatsheet][] to learn the basical
commands.

## vim plugins

Start by installing [pathogen.vim][], a vim plugin manager:

```
mkdir -p ~/.vim/autoload ~/.vim/bundle && \
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
```

Then add this to your vimrc:

```
execute pathogen#infect()
```

From now on, every plugin that is compatible with pathogen can be simply
installed by cloning its repo at `~/.vim/bundle`.

An alternative for pathogen is [vundle][]. Haven't used it but it
behaves similarly.

### rails.vim

Probably the one most useful plugin when dealing with Rails projects.

Install it with:

```
git clone git://github.com/tpope/vim-rails.git ~/.vim/bundle/vim-rails
```

**Browsing through the app**

You can use `:RController foos` and it will take you straight
to the `app/controllers/foos_controller.rb`. As you might guess, same
happens with `:RModel foo`, etc. There is also tab completion so that
you can toggle between all models/controllers, etc.

Another useful command is `:find`. Invoking it with a name foo, it first
searches for a model named foo. Tab completion is also your friend.

One other really cool feature is the go to file. Supposedly we have the
following model:

```ruby
class Blog < ActiveRecord::Base

  has_many :articles

end
```

Placing the cursor on the articles word and pressing `gf` vim opens
the article model. After saving your changes you can go back to the blog
model by pressing `Ctrl-o`.

**Run your tests through vim**

Running test is also a matter of a command. Say you are editing a specific
spec/test file. All you have to do is run `:Rake` and the tests for that
particular file will be ran, without leaving your favorite editor :)

The supported commands are a lot and your best bet is to invoke
`:help rails` in vim and learn about them.

Be sure to also check [vim-rails][] on github.

### vim-snipmate

SnipMate implements snippet features in Vim. A snippet is like a template,
reducing repetitive insertion of pieces of text. Snippets can contain
placeholders for modifying the text if necessary or interpolated code for
evaluation.

Install it:

```
cd ~/.vim/bundle
git clone https://github.com/tomtom/tlib_vim.git
git clone https://github.com/MarcWeber/vim-addon-mw-utils.git
git clone https://github.com/garbas/vim-snipmate.git
git clone https://github.com/honza/vim-snippets.git
```

- [List of supported Ruby snippets][ruby-snippets]
- [List of supported Rails snippets][rails-snippets]

**Writing a method**

Reading the source code of snippets above let's see how we can create a
method. The snippet reads:

```
snippet def
        def ${1:method_name}
                ${0}
        end
```

So, the snippet is named `def` and in order to invoke it we must write
def and hit Tab. It then expands, placing the cursor in the highlited
`method_name`. This is what it looks like:

```
def method_name
  
end
```

Once you start typing, method_name gets replaced with what you type. When
you finish, hit Tab again to go to the method body.

Now all you have to do is read the `ruby.snippet` and find out what
snippets are supported.

### fugitive.vim

[vim-fugitive][] brings the power of git commands inside vim.

Install it with:

```
git clone git://github.com/tpope/vim-fugitive.git ~/.vim/bundle/vim-fugitive
```

Check out the github page for a list of commands and some interesting
screencasts.

# Terminal multiplexer (tmux)

Again, here you have two options. `screen` or `tmux`. My first contact was
with screen but recently I decided to try tmux.

I won't go into any details but I highly reccomend watching Chris Hunt's
presentation [Impressive Ruby Productivity with Vim and Tmux][tmux-u].
It's an awesome talk.

# Development stack

There is a great [article][] I stumbled upon yesterday about some must have gems
for development, some of which I haven't tested. Here is what I got so far.

## jazz_hands

[jazz_hands][] is basically a collection of gems that you get for free with
just one gem. It focuses on enhancing the rails console. It provides:

```
- Pry for a powerful shell alternative to IRB.
- Awesome Print for stylish pretty print.
- Hirb for tabular collection output.
- Pry Rails for additional commands (show-routes, show-models, show-middleware) in the Rails console.
- Pry Doc to browse Ruby source, including C, directly from the console.
- Pry Git to teach the console about git. Diffs, blames, and commits on methods and classes, not just files.
- Pry Remote to connect remotely to a Pry console.
- Pry Debugger to turn the console into a simple debugger.
- Pry Stack Explorer to navigate the call stack and frames.
- Coolline and Coderay for syntax highlighting as you type. Optional. MRI 1.9.3/2.0.0 only
```

Again, visiting the github page, you will get all the info you want.
There is an open [issue][] and installation on ruby 2.1.2 is failing for now.
For the time being you can put the following in your Gemfile:

```
gem 'jazz_hands', github: 'nixme/jazz_hands', branch: 'bring-your-own-debugger'
gem 'pry-byebug'
```

## rubocop

[rubocop][] is a tool which checks if your code conforms to the
[ruby][ruby-guide]/[rails][rails-guide] community guidelines.

You can check the article I [wrote]({filename}./2014-06-16-rubocop-to-the-rescue.md)
where I explain how to set it up and running.

## railroady

[railroady][] is a tool that lets you visualize how the models and the
controllers of your app are structured. Instructions on how to install it are
on the github page. You can [check][railroady-fruby] how it looks like on the
fedoraruby project I'm currently working on.

## annotate

[annotate][] generates a schema of the model and places it on top of the model.
It can also place it on top of your rspec files and the factories. It looks
like this:

```
# == Schema Information
#
# Table name: bugs
#
#  id            :integer          not null, primary key
#  name          :string(255)
#  bz_id         :string(255)
#  fedora_rpm_id :integer
#  is_review     :boolean
#  created_at    :datetime
#  updated_at    :datetime
#  last_updated  :string(255)
#  is_open       :boolean
#
```

# Testing stack

There is a ton of useful tools out there and if you are new to rails
development you can easilly get lost. [Rails has Two Default Stacks][] is
a nice read that sums it up. I will try to update this post as I find more
useful tools in my way.

## rspec

I am mostly in favor of rspec because of its descriptive language and the great
support by other complement testing tools.

## capybara

So, why capybara and not cucumber? I'm not an expert on neither of these tools
but from my understanding capybara is more focused on developers whereas
cucumber's human language mostly targets aplications where one talks to a
non-technical customer.

## guard

> Guard watches files and runs a command after a file is modified. This allows
> you to automatically run tests in the background, restart your development
> server, reload the browser, and more.

It has nearly 200 plugins which provide different options as guard is not only
used for testing. The particular plugin for rspec is [guard-rspec][].

When you make the smallest change to a test and you hit save, [guard][] will
run that particular test group again to see if it still passes.

I tend to invoke guard with `guard -c` which runs the tests in a clear console
every time.

Read the [guard wiki page][] which is comprehensive and also watch the
[guard railscast][] to better understand it.

# Other super useful tools

## ctags

Quoting from [What is ctags?][whatis]:

> Ctags generates an index (or tag) file of language objects found in
> source files that allows these items to be quickly and easily located
> by a text editor or other utility.

There are a bunch of different tools to create a tags file, but the most
common implementation is [exuberant ctags][exuberant] which we will use.

It supports 41 programming languages and a handful of editors.
directories
### Installation

Install ctags via your package manager. It should be supported in all
major ditributions.

### Configuration

For a rails project, in your application root directory you can run:

```
ctags -R --exclude=.git --exclude=log *
```

This searches recursively all files in the current directory, excludes
the `.git` and `log` directories and creates a `tags` file under current
dir. You may want to add it to `.gitignore` by the way.

Next, adding the following line to `~/.vimrc`:

```
set tags=./tags;
```

sets the location of the tags file, which is relative to the current
directory.

You can move the above options in `~/.ctags`, so in our case this will
be:

```
--recurse=yes
--tag-relative=yes
--exclude=.git
--exclude=log
```

So in future runs of ctags all you need to do is `ctags *`.

ctags doesn't autogenerate, so each time you write code that is tagable,
you have to run the command again. If you are working in a git repository
be sure to checkout Tim Pope's [Effortless Ctags with Git][ctags-hooks].
What this does is:

> Any new repositories you create or clone will be immediately indexed
> with Ctags and set up to re-index every time you check out, commit,
> merge, or rebase. Basically, you’ll never have to manually run Ctags
> on a Git repository again.

### Usage

Say we have a file containing hundrends of lines. Inside a method you
see the below definition:

```ruby
def contain_multiple_methods
  method_one
  method_two
  method_three
end
```

While you could search for these methods, you can save a few keystrokes
by simply getting the cursor on the line of the method to search and in
vim normal mode press `Ctrl + ]` (control and right square bracket).
This should get you where the method is. Go back to where you were by
pressing `Ctrl + t`.

**Note:** The usage of ctags isn't restricted only in the current file.
If a method in your file is inherited by another class, then searching
for it will jump in this particular file.

### Secret power

Wouldn't it be cool if we could search for methods in the Rails source
code? Here is where the power of ctags really excels. All you have to do
is tell ctags to also tag the rails source code.

First I cloned the rails repository into `vendor/rails`:

```
git clone https://github.com/rails/rails.git vendor/rails
```

It should take less than a minute to download. You wouldn't want
the rails source code to be included in your git tree, so you simply
exclude `vendor/rails` by adding it to `.gitignore`.

Lastly, create again the tags with `ctags *`.

Now navigate with vim to one of your models that has for example the
association `has_many`, place the cursor on it (or just on the same line)
and hit `Ctrl + ]`. Pretty cool huh? In case you forgot, go back to where
you were with `Ctrl + t`.

## ack

[ack][] is like grep but on steroids.

> Designed for programmers with large heterogeneous trees of source code,
> ack is written purely in portable Perl 5 and takes advantage of the
> power of Perl's regular expressions.

It supports multiple types which you can see by typong `ack --help-types`.

Of course there is a [vim plugin][ack-vim]!

### alternative (ag)

While reading the [more-tools][] page of ack I found out about [ag][],
also called the_silver_searcher. It is said to search code about 3–5×
faster than ack, is written in C and have some more enhancements than ack.
You may want to give this a try to. And as you have guessed there is also
an [ag vim plugin][ag-vim].

# Conclusion

The editor of choice and the tools you use in web development play a great role
in one's productivity, so you have to choose wisely and spend some time to get
to know it. Personally, I learned a lot more these past days I was crafting
this post and I hope you got something out of it too :)

[article]: http://www.codebeerstartups.com/2013/04/must-have-gems-for-development-machine-in-ruby-on-rails
[rubocop]: https://github.com/bbatsov/rubocop
[codeschool]: https://codeschool.com "codeschool homepage"
[Vim for Rails Developers]: https://learn.thoughtbot.com/products/2-vim-for-rails-developers "Vim for Rails Developers"
[guard wiki page]: https://github.com/guard/guard/wiki "guard wiki page"
[guard-railscast]: http://railscasts.com/episodes/264-guard "guard on railscasts"
[guard-rspec]: https://github.com/guard/guard-rspec "guard-rspec on github"
[guard]: https://github.com/guard/guard "guard on github"
[issue]: https://github.com/nixme/jazz_hands/pull/26
[jazz_hands]: https://github.com/nixme/jazz_hands "jazz_hands on github"
[annotate]: https://github.com/ctran/annotate_models "annotate on github"
[railroady-fruby]: https://gitlab.com/fedora-ruby/isitfedoraruby/raw/master/doc/models_complete.svg
[railroady]: https://github.com/preston/railroady "railroady gem"
[ruby-guide]: https://github.com/bbatsov/ruby-style-guide "Ruby style guide"
[rails-guide]: https://github.com/bbatsov/rails-style-guide "Rails style guide"
[Rails has Two Default Stacks]: http://words.steveklabnik.com/rails-has-two-default-stacks "Rails has Two Default Stacks"
[tmux-u]: https://www.youtube.com/watch?v=9jzWDr24UHQ "Chris Hunt - Impressive Ruby Productivity with Vim and Tmux - Ancient City Ruby 2013 "
[ruby-snippets]: https://github.com/honza/vim-snippets/blob/master/snippets/ruby.snippets "Ruby supported snippets"
[rails-snippets]: https://github.com/honza/vim-snippets/blob/master/snippets/ruby.snippets#L598 "Rails supported snippets"
[vim-fugitive]: https://github.com/tpope/vim-fugitive "vim-fugitive on github"
[vim-rails]: https://github.com/tpope/vim-rails "vim-rails on github"
[cheatsheet]: http://www.viemu.com/vi-vim-cheat-sheet.gif "vim cheatsheet"
[vundle]: https://github.com/gmarik/Vundle.vim "vundle vim plugin"
[pathogen.vim]: https://github.com/tpope/vim-pathogen "pathogen vim plugin"
[ack-vim]: https://github.com/mileszs/ack.vim "ack vim plugin"
[ag-vim]: https://github.com/rking/ag.vim "ag vim plugin"
[more-tools]: http://beyondgrep.com/more-tools/ "ack: more tools"
[ag]: https://github.com/ggreer/the_silver_searcher "ag at github"
[ack]: http://beyondgrep.com/ "ack homepage"
[ctags-hooks]: http://tbaggery.com/2011/08/08/effortless-ctags-with-git.html "Effortless Ctags with Git"
[exuberant]: http://ctags.sourceforge.net/ "Exuberant ctags homepage"
[whatis]: http://ctags.sourceforge.net/whatis.html "What is ctags?"
