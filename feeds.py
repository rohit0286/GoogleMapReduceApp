"""File contains handlers for feeds."""

__author__ = 'rohit0286@gmail.com (Rohit Sharma).'

from datetime import datetime as date_time
from index_mapreduce import index
import feedparser
import models
import settings
import utils
import webapp2


class Feed(webapp2.RequestHandler):
  """Contains handlers for saving and rendering feeds."""

  def post(self):
    """Renders feeds_view html."""
    action = self.request.POST.get('action')
    if action == 'getfeedsbytags':
      tag_str = self.request.POST.get('tags')
      tags = tag_str.split(' ')
      feeds = self._GetFeedsByTagNames(tags)
      payload = {'feeds': feeds}
      return utils.RenderTemplate('feeds_view.html',
                                  self.response, payload)

  def get(self):
    """Renders feed_view or saves feeds from sources."""
    action = self.request.GET.get('action')
    if action == 'import':
      rss_sources = models.RSSSource.GetAllSources()
      for rss_source in rss_sources:
        self._SaveFeeds(rss_source.url)
      return self.redirect('/feeds')
    if action == 'flushall':
      models.Feed.DeleteAll()
      models.Tag.DeleteAll()
      return webapp2.Response('All Feeds and Tags removed.')
    else:
      feeds = models.Feed.GetAllFeeds()
      payload = {'feeds': feeds}
      return utils.RenderTemplate('feeds_view.html',
                                  self.response, payload)

  def _GetFeedsByTagNames(self, tags):
    """Returns feed by tag names.
    Args:
      tags: A list containing tag names.
    Returns:
      An iterable containing feeds.
    """
    tags_keys = []
    for tag_name in tags:
      tag = models.Tag.GetTagByName(tag_name.lower())
      if tag:
        tags_keys.append(tag.key())
    return models.Feed.GetFeedsByTags(tags_keys)

  def _SaveFeeds(self, feed_url):
    """Save feed into storage.
    Args:
      feed_url: Url of feed source.
    """
    feeds = feedparser.parse(feed_url)
    entries = feeds.get('entries', [])
    for feed_json in entries:
      title = feed_json.get('title')
      pub_date = date_time.strptime(
        feed_json.get('published'),
        '%a, %d %b %Y %H:%M:%S +0000')
      if not self._FeedExists(pub_date, title):
        models.Feed.AddFeed(feed_json)

  def _FeedExists(self, published_date, title):
    """Checks if a feed exists.
    Args:
      published_date:  Published date of a feed.
      title: Title of a feed.
    Returns:
      True if feed exists else False.
    """
    feed = models.Feed.GetFeed(['title',
                                'published_date'],
                               [title, published_date])
    return True if feed else False

