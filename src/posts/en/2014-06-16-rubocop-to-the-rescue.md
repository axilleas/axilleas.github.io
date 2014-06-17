Title: Rubocop to the rescue!
Slug: rubocop-to-the-rescue
Tags: fedora, isitfedoraruby, gsoc, ruby, rails, webdev, rubocop
Category: geek
Lang: en

*I decided to drop the GSoC related titles and focus on the things
that I work during the week. That means I'll probably blog more often :p*

This week I mostly focused on cleaning the code of [fedoraruby][] and
conforming to the [ruby][ruby-guide]/[rails][rails-guide] community
guidelines.

The gem that helps you do that is [rubocop][] and is kind of the standard
method in the ruby world.

[TOC]

# RuboCop

Rubocop refers to each check as a cop. There are a bunch and you can see
the supported ones by reading these [files][rubo-enabled].

After installing rubocop, call it with the `rubocop` command and it
will check all Ruby source files in the current directory.

If working on a Rails project, you have to invoke it with the `-R` flag.

The first time I ran rubocop I was presented with no more or less
**666** violations. Which meant if I wanted to clean up the code I'd had to
manually edit all 666 of them. Luckily, as you may have imagined, rubocop
provides the `-a/--auto-correct` flag which does what it says. In the
documentation there is a note: *Experimental - use with caution*. What the
heck, I had nothing to lose, I am under version control so I could go back
any time. It worked like a charm and this brought the violations to about
**150**. Not bad at all.

So what about the rest? Well, you have to do it manually and so I began.
If you run rubocop without any flags, it uses the [default config][rubo-conf] that
ships with the gem. If you want to use your config you can do so by defining
it with the `-c` flag.

Now, there is another cool feature rubocop provides. It can create a config
file for you containing all the violations found so far. Run rubocop with
the `--auto-gen-config` flag and that will create `.rubocop_todo_yml` in
the current dir. Then you can check against that file with
`rubocop -R -c .rubocop_todo_yml`.

All cops in this yaml file are set to false, which means they won't be taken
into account, not unless you explicitly set them to true. That way you can
work your way up in fixing all violations by enabling one cop at a time.
Basically what is included in this file, overrides the default values.

If you want to omit calling on `.rubocop_todo_yml` every single time, place
this in `.rubocop.yml`:

    inherit_from: .rubocop_todo.yml

Form now on you can just call it with `rubocop -R`.

To sum up, run `rubocop -R` see that there is no violation, edit
`.rubocop_todo_yml`, set one of the cops to true, run rubocop again, fix
the errors and work your way up until there is no violation.

Of course all of these are optional steps. Ruby's interpreter doesn't care
about identation, it won't complain if you run a method 20 lines long and
it won't throw an error if you have chain 16 methods spanning to 300 chars.
All these are conventions among the Ruby community and you are not compelled
to follow them. BUT, it provides much cleaner code and when you find yourself
contributing to a project, all these will probably matter.

In my case, you can see through [this commit][commit] what changed and in
this [gist][] you can see the difference from before/after running rubocop.
Dropped to 73 violations from 666.

I've skipped some of them as I didn't see fit, like commenting above every
class what it does. I'm not saying this isn't good to have it's just it
also includes migrations and I'd like to avoid that. Also some code will
be deprecated/rewritten any time soon so it doesn't make sense to fix the
violations if I'm to remove the code afterwards.

# HoundCI

Rubocop is good to test locally, but what about the code you host remotely?
Enter [Houndci][].

Houndci is a web app written in Rails by [Thoughtbot][] that integrates with
your github account. It checks for violations every time a Pull Request is
submited against your repository. It relies on the rubocop gem, but it
may follow [different][hound-style] approaches than rubocop.

I almost spent a day to find this out. I'll tell you what I mean since there
was a particular error that made me search for many hours.

Let's start by saying that it is common practice to not have lines spanning
on more that 80 characters. [Python][pep8] has it pinned to 79.

In rubocop, there is a cop that checks for method chaining. When the line
is too long you should break it down, so this cop checks whether the 
dot(**.**) that chains two methods is placed before or after the methods.
Here's an example to better visualize it:

```ruby
def method_with_arguments(argument_one, argument_two)
  a_really_long_line_that_is_broken_up_over_multiple_lines_and.
  subsequent_lines_are_indented_and.
  each_method_lives_on_its_own_line
end

```

When I ran rubocop locally it complained with *Place the . on the next line, together with the method name.*
Ok I did that and pushed. Then why was houndci told me [otherwise][dotwarn]?

Digging in rubocop's default [config][dot-config] file I found that this particular
cop was invoking an additional parameter: `EnforcedStyle: leading`.
Interesting, so why houndci was telling me the opposite? Digging some more,
this time in rubocop's source code, I found the responsible [method][].
It seems rubocop gives you the option to decide which style fits you better
and from what I've seen so far, houndci prefered the trailing dot. Ok let's
fix that.

Reading the [configuration][hound-conf] guide, and since houndci uses rubocop, I
copied `.rubocop_todo_yml` to `.hound.yml`. There, following the [config][dot-config]
file I appended

```
Style/DotPosition:
  EnforcedStyle: leading
  Enabled: true
```

in `.hound.yml`, pushed the change to my repo and created a test pull request
to check if it worked. No... but whyyyy??

After some more more digging, this time at the issue tracker of houndci,
I finally found the [culprit][]. The latest version of rubocop [changed][]
the way cops are presented and that broke compatibility with houndci.
Back to `.hound.yml` I removed `Style/` and pushed to github. Finally,
this time it was fixed.

Not much of a story, probably you already got bored or didn't make it this
far, but anyway. Onto more interesting stuff, until next time it is.


[changed]: https://github.com/bbatsov/rubocop/blob/master/relnotes/v0.23.0.md "Rubocop 0.23.0 release notes"
[hound-style]: https://github.com/thoughtbot/guides/tree/master/style "Thoughtbot style guide"
[culprit]: https://github.com/thoughtbot/hound/issues/288 "Hound not picking up changes in .hound.yml"
[hound-conf]: https://houndci.com/configuration "Hound configuration"
[method]: https://github.com/bbatsov/rubocop/blob/master/lib/rubocop/cop/style/dot_position.rb#L22 "cop that checks the . position in multi-line method calls."
[dot-config]: https://github.com/bbatsov/rubocop/blob/master/config/default.yml#L187 "Default configuration about the dot position cop"
[dotwarn]: https://github.com/axilleas/isitfedoraruby/pull/1#discussion-diff-13786984 "HoundCI complaining on dot"
[ruby-guide]: https://github.com/bbatsov/ruby-style-guide "Ruby style guide"
[rails-guide]: https://github.com/bbatsov/rails-style-guide "Rails style guide"
[fedoraruby]: https://github.com/axilleas/isitfedoraruby "isitfedoraruby at github"
[rubocop]: https://github.com/bbatsov/rubocop "rubocop at github"
[Houndci]: https://houndci.com/ "HoundCI website"
[Thoughtbot]: http://robots.thoughtbot.com/ "Thoughtbot website"
[rubo-conf]: https://github.com/bbatsov/rubocop/tree/master/config "Default configuration files for rubocop"
[commit]: https://github.com/axilleas/isitfedoraruby/commit/0a39c2b1a3d3aa47433c52147fe9ecb443e3ea98 "Commit fixing most of rubocops errors"
[pr]: https://github.com/axilleas/isitfedoraruby/pull/1 "Pull Requestfixing most of rubocops errors "
[gist]: https://gist.github.com/axilleas/b65a909a5d0b73fcb2a8 "gist with before/after violations"
[pep8]: http://legacy.python.org/dev/peps/pep-0008/#maximum-line-length "Python PEP8 maximum line length"