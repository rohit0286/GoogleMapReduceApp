"""File contains mappings of url and handlers."""

import feeds
import index_views
from google.appengine.ext.webapp.util import run_wsgi_app
import warmup
import webapp2
from index_mapreduce import index


application = webapp2.WSGIApplication([
    ('/', feeds.Feed),
    ('/feeds', feeds.Feed),
    ('/index', index_views.FeedsIndexer),
    ('/_ah/warmup', warmup.Warmup),
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()