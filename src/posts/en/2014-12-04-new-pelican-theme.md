Title: Redesigning the looks of this blog
Slug: pelican-new-theme-redesign
Tags: pelican, python, css, jinja, fedoraplanet
Category: opensource
Lang: en

It's been a long time since last I showed some love for the UI of this blog,
and after a day of modifications I'm pretty excited about the outcome :w00t:

So, what has changed?

[TOC]

## UI redesign

I like simple things and I always wanted the same thing for my blog. Few years
ago, I had come across a static site built with [jekyll][] and loved its
simplicity. My new theme is heavilly inspired by <http://uberspot.github.io>,
hence the name I decided to give it. This nice feature of rotating pictures
with every new visit isn't implemented yet for pelican, but it's in my plans.

[Vincent Bernat's blog][luffy] has also been an inspiration and you'll see
many css styles taken from there, for example the table of contents. Apart
from design patterns, he is writing some very cool stuff so I urge you to
follow him.

I prefer the light themes over the darks ones, but not too bright. The
background is taken from [subtle patterns][], an awesome site that has many
patterns to choose from. I went with [paper fibers][] and I like the outcome so
far.

The main font used is [Merriweather][] from Google's webfonts and was inspired
to use by Vincent's blog.

Code blocks are styled after Mozilla's Developer Network, here is a sample
taken form [here][mdn]:

```javascript
var foo = 42;    // foo is a Number now
var foo = "bar"; // foo is a String now
var foo = true;  // foo is a Boolean now
```

[pygments][] is used underneath and I picked the [friendly][] style.

Blockquotes are restyled to use sharp edges and a light orange color:

> Look, let me explain something. I'm not Mr. Lebowski. You're Mr. Lebowski.
> I'm the Dude. So that's what you call me. That, or Duder, or His Dudeness, or
> El Duderino, if you're not into the whole brevity thing.

## New plugins used

Pelican has a very active community and its powerful structure make it dead
easy to add a plugin or even write your own. Head over the [pelican-plugins][]
repo and see your options.

For the time being I chose to use three plugins that add some pretty nice
functionality to the UI and UX.

### search

Being a static site, the only way to add some search functionality is
by using javascript. Thankfully, there is a jquery plugin that does exactly
that and is named [tipue search][]. Some nice guy provided a pelican plugin
so I took a shot and used it.

There isn't much information in the docs how to set it up, but after a little
search, I found some articles that explained it in depth.

- <http://moparx.com/2014/04/adding-search-capabilities-within-your-pelican-powered-site-using-tipue-search/>
- <http://www.futurile.net/2014/04/19/sitesearch-for-pelican-blog-with-tipue/>

### neighboring articles

The [neighbors plugin][] adds `next_article` (newer) and `prev_article` (older)
variables to the article's context.

As you'll see I added some nice bowling pins icons to show you the way :)

### post statistics

A really nice plugin is the [post_stats][] which calculates various statistics
about a post and stores them in an `article.stats` dictionary.

Now you get the average time to read a post, and if you hover over it, you also
see the total words written.

## Source code

As always, the [source code][] is available to take a look and hack on.
I haven't yet submitted it to the pelican-themes repo as I need to sort some
things and clean it up a bit.

[subtle patterns]: http://subtlepatterns.com/ "Free to use tilable textured patterns"
[jekyll]: http://jekyllrb.com/ "Jekyll - Static blog generator"
[luffy]: http://vincent.bernat.im/en/ "Disruptive ninja - Vincent Bernat"
[paper fibers]: http://subtlepatterns.com/paper-fibers/
[Merriweather]: https://www.google.com/fonts "Google webfonts"
[tipue search]: http://www.tipue.com/search/docs/ "A site search engine jQuery plugin"
[neighbors plugin]: https://github.com/getpelican/pelican-plugins/tree/master/neighbors "Pelican neighbors plugin"
[pelican-plugins]: https://github.com/getpelican/pelican-plugins "Pelican plugins GitHub repo"
[post_stats]: https://github.com/getpelican/pelican-plugins/tree/master/post_stats "post stats pelican plugin"
[source code]: https://github.com/axilleas/pelican-uberspot "Pelican uberspot theme"
[mdn]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Dynamic_typing
[pygments]: http://pygments.org/ "Python syntax highlighter"
[friendly]: http://pygments.org/demo/218030/?style=friendly "friendly pygments style"
