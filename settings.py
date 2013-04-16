# -*- coding: utf-8 -*- #
from hashlib import md5

AUTHOR = u"axil"
AUTHOR_SHORTBIO = '''
I'm an open source enthousiast who loves spaghetti and westerns.
Currently I am struggling to graduate and get involved in as many
projects as I can :)
'''
SITENAME = u"Over the line"
SITEURL = 'http://axilleas.github.io'
SITE_TAGLINE = u'that rug really tied the room together...'
TIMEZONE = 'Europe/Athens'

GITHUB_URL = 'http://github.com/axilleas'
GITHUB_USERNAME = 'axilleas'
GITHUB_BADGE = True
DISQUS_SITENAME = 'kissmyarch'
TWITTER_USERNAME = '_axil'
#PDF_PROCESSOR = True
PRINT = True
REVERSE_CAREGORY_ORDER = True
LOCALE = ('usa', 'en_US')
DEFAULT_LANG = 'en'
DEFAULT_PAGINATION = 3
SITE_SOURCE = 'https://github.com/axilleas/axilleas.github.io/tree/source'

AUTHOR_EMAIL = u'axilleas@archlinux.gr'
AUTHOR_EMAIL_HASH = md5(AUTHOR_EMAIL).hexdigest()

FEED_DOMAIN = SITEURL
FEED_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
TAG_FEED_RSS = 'feeds/%s.rss.xml'

MD_EXTENSIONS = ['toc', 'codehilite', 'extra']
THEME = "src/theme"

OUTPUT_PATH = 'output'
PATH = 'src'

STATIC_PATHS = ['images', 'files']

ARTICLE_EXCLUDES = ('pages','drafts',)
ARTICLE_URL = "{lang}/blog/{date:%Y}/{slug}"
ARTICLE_SAVE_AS = "{lang}/blog/{date:%Y}/{slug}/index.html"
ARTICLE_LANG_URL = "{lang}/blog/{date:%Y}/{slug}"
ARTICLE_LANG_SAVE_AS = "{lang}/blog/{date:%Y}/{slug}/index.html"

DISPLAY_PAGES_ON_MENU = True
PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}/index.html"
PAGE_LANG_URL = "{lang}/{slug}"
PAGE_LANG_SAVE_AS = "{lang}/{slug}/index.html"

PIWIK_URL = 'animal.foss.ntua.gr/~axil/stats'
PIWIK_SITE_ID = 5
