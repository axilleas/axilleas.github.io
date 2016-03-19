# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u"axil"
SITENAME = u"Over the line"
SITEURL = 'http://axilleas.me'
SITE_TAGLINE = u"Yeah, well, you know, that's just, like, my opinion, man."
TIMEZONE = 'Europe/Athens'
SHOW_AUTHOR = False

LOCALE = ('en_US.utf8')
DEFAULT_LANG = 'en'
SITE_SOURCE = 'https://gitlab.com/axil/axil.gitlab.io'

FEED_DOMAIN = SITEURL
FEED_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
TAG_FEED_RSS = 'feeds/%s.rss.xml'

MD_EXTENSIONS = ['toc', 'codehilite', 'extra']
THEME = "../pelican-uberspot"

OUTPUT_PATH = 'public'
PATH = 'content'

STATIC_PATHS = ['images', 'files']

ARTICLE_EXCLUDES = ('pages','drafts',)
ARTICLE_URL = "{lang}/blog/{date:%Y}/{slug}"
ARTICLE_SAVE_AS = "{lang}/blog/{date:%Y}/{slug}/index.html"
ARTICLE_LANG_URL = "{lang}/blog/{date:%Y}/{slug}"
ARTICLE_LANG_SAVE_AS = "{lang}/blog/{date:%Y}/{slug}/index.html"

PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}/index.html"
PAGE_LANG_URL = "{lang}/{slug}"
PAGE_LANG_SAVE_AS = "{lang}/{slug}/index.html"

PLUGIN_PATHS = ['../pelican-plugins']

PLUGINS = [
    'pelicanfly',
    'post_stats',
    'tipue_search',
    'neighbors',
#    'filetime_from_git',
]

DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'authors', 'archives', 'search'))

DISQUS_SITENAME = 'kissmyarch'
PIWIK_URL = 'piwik2-glb.rhcloud.com'
PIWIK_SITE_ID = 5
