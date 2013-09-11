"""Models of Feeds."""

__author__ = 'rohit0286@gmail.com (Rohit Sharma)'

from datetime import datetime as date_time
from google.appengine.ext import db


class Feed(db.Model):
  """Describes a feed.

  Properties:
    title: Title of a feed.
    url: Url of a feed.
    description: Description of feed.
    published_date: Published date of a feed.
  """
  title = db.StringProperty()
  url = db.URLProperty()
  description = db.TextProperty()
  published_date = db.DateTimeProperty()
  tags = db.ListProperty(db.Key)

  @classmethod
  def AddFeed(cls, feed_json):
    """Adds a feed from json to db.
    Args:
      feed_json: Json containing feed data.
    Returns:
      Key of added feed item.
    """
    feed_item = Feed()
    feed_item.title = feed_json.get('title')
    feed_item.url = feed_json.get('link')
    feed_item.description = feed_json.get('description')
    pub_date = date_time.strptime(
        feed_json.get('published'),
        '%a, %d %b %Y %H:%M:%S +0000')
    feed_item.published_date = pub_date
    return feed_item.put()

  @classmethod
  def GetAllFeeds(cls, only_keys_required=False):
    """Returns a query object containing all feeds.
    Args:
      only_keys_required: Boolean param depicting if only
      feed keys are required.
    Returns:
      Query object contaning required feeds.
    """
    return cls.all(keys_only=only_keys_required).order(
        'published_date').order('title')

  @classmethod
  def GetFeed(cls, filters, values):
    """Returns feeds on the basis of filters and values.
    Args:
      filters: A list containing filters.
      values: A list containing filter values.
    Returns:
      Feed as per required filters.
    """
    feed_query = cls.all()
    for filter, value in zip(filters, values):
      feed_query.filter( filter +' =', value)
    return feed_query.get()

  @classmethod
  def GetFeedsByTags(cls, tags_keys=None):
    """Returns feed by tags.
    Args:
      tags_keys: A list containing tag keys.
    Returns:
      A list containing required feeds.
    """
    feeds = cls.all().filter('tags IN', tags_keys).order(
        'published_date').order('title')
    return feeds

  def AddTagByKey(self, tag_key_or_str):
    """Adds a tag to feed.
    Args:
      tag_key: Key of tag.
    Raises:
      TypeError: If tag key is not string or db.Key object.
    """
    tag_key = None
    if isinstance(tag_key_or_str, basestring):
      tag_key = db.Key(tag_key_or_str)
    elif isinstance(tag_key_or_str, db.Key):
      tag_key = tag_key_or_str
    if tag_key:
      self.tags.append(tag_key)
      self.put()
    else:
      raise TypeError('Tag key should either be string or db.Key')

  def AddTagByName(self, name):
    """Adds a tag to feed by name.
    Args:
      name: Name of the tag.
    """
    tag = Tag.GetTagByName(name)
    if tag:
      self.AddTagByKey(tag.key())

  @classmethod
  def DeleteAll(cls):
    db.delete(cls.all())

class Tag(db.Model):
  """Describes a tag.

  Properties:
    name: Name of a tag.
  """
  name = db.StringProperty()

  def GetAllTags(cls):
    """Returns a query object containing tags."""
    return cls.all().order('name')

  @classmethod
  def AddTag(cls, tag_name):
    """Creates a new tag.
    Args:
      tag_name: Name of the tag.
    Returns:
      Key of the saved tag.
    """
    tag_key = cls.GetTagByName(tag_name, True)
    if not tag_key:
      tag = Tag()
      tag.name = tag_name
      tag_key = tag.put()
    return tag_key

  @classmethod
  def GetTagByName(cls, name, only_keys_required=False):
    """Returns a tag by name."""
    tag = Tag.all(keys_only=only_keys_required).filter(
        'name =', name).get()
    return tag

  @classmethod
  def DeleteAll(cls):
    db.delete(cls.all())

class RSSSource(db.Model):
  """Describes a RSS Feed Source.

  Properties:
    name: Name of a RSS feed source.
    url: url of a RSS feed source.
  """
  name = db.StringProperty()
  url = db.URLProperty()

  @classmethod
  def GetAllSources(cls):
    """Returns a query object of all RSS feed sources."""
    return cls.all().order('name')

  @classmethod
  def GetSourceByName(cls, name):
    """Returns a RSS Feed source.

    Args:
      name: Name of RSS source.

    Returns:
      A RSS source or None.
    """
    return cls.all().filter('name =', name).get()

  @classmethod
  def AddSource(cls, source_json):
    """Adds a RSS source.

    Args:
      source_json: A Json containing RSS source data.

    Returns:
      Key of saved RSS source.
    """
    rss_source = RSSSource()
    rss_source.name = source_json.get('name')
    rss_source.url = source_json.get('url')
    return rss_source.put()

  def UpdateSource(self, source_json):
    """Updates a RSS source.

    Args:
      source_json: A Json containing RSS source data.

    Returns:
      Key of an updated RSS source.
    """
    self.name = source_json.get('name')
    self.url = source_json.get('url')
    return self.put()

