# -*- coding: utf-8 -*- #
from hashlib import md5

AUTHOR = u"axil"
AUTHOR_SHORTBIO = '''
I'm an open source enthousiast. I love spaghetti and westerns.
'''
SITENAME = u"Over the line"
SITEURL = 'http://axilleas.github.com'
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
SITE_SOURCE = 'https://github.com/axilleas/axilleas.github.com/tree/source'

FEED_DOMAIN = SITEURL
FEED_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
TAG_FEED_RSS = 'feeds/%s.rss.xml'

MD_EXTENSIONS = ['toc', 'codehilite', 'extra']
THEME = "src/theme"

OUTPUT_PATH = 'output'
PATH = 'src'

STATIC_PATHS = ['images', '']

ARTICLE_EXCLUDES = ('pages','drafts',)
ARTICLE_URL = "{lang}/blog/{date:%Y}/{slug}/"
ARTICLE_SAVE_AS = "{lang}/blog/{date:%Y}/{slug}/index.html"

DISPLAY_PAGES_ON_MENU = True
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
PAGE_LANG_URL = "{lang}/{slug}/"
PAGE_LANG_SAVE_AS = "{lang}/{slug}/index.html"




