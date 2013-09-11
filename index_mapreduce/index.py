"""File contains map reduce functions and accessories."""

__author__ = 'rohit0286@gmail.com (Rohit Sharma).'

import logging
import models
import re

from mapreduce import base_handler
from mapreduce import mapreduce_pipeline
from mapreduce import operation as op
from mapreduce import shuffler


def index_map(feed):

  def SanitizeFeed(feed_text):
    unicoded_text = feed_text
    unicoded_text = feed_text.encode('utf-8')
    text_no_tags = re.sub(r'<[^<]+?>', '', unicoded_text)
    sanitized_feed_text = re.sub('[\\?\'?\"?\.?]', '',
                                 text_no_tags)
    sanitized_feed_text = sanitized_feed_text.replace('\n',
                                                      ' ')

    return sanitized_feed_text.lower()

  feed_text = '{0} {1}'.format(
      SanitizeFeed(feed.title),
      SanitizeFeed(feed.description))
  for word in feed_text.split(' '):
    try:
      tag_key = models.Tag.AddTag(word)
      yield(tag_key, str(feed.key()))
    except UnicodeDecodeError:
      pass

def index_reduce(tag_key, feeds):
  for feed_key in feeds:
    feed = models.Feed.get(feed_key)
    feed.AddTagByKey(tag_key)

class IndexPipeline(base_handler.PipelineBase):
  """A pipeline to run indexing.

  Args:
    blobkey: blobkey to process as string. Should be a zip archive with
      text files inside.
  """

  def run(self):
    yield mapreduce_pipeline.MapreducePipeline(
        'IndexingMapReduce',
        'index_mapreduce.index.index_map',
        'index_mapreduce.index.index_reduce',
        'mapreduce.input_readers.DatastoreInputReader',
        'mapreduce.output_writers.BlobstoreOutputWriter',
        mapper_params={
            'entity_kind': 'models.Feed',
        },
        reducer_params={
            'mime_type': 'text/plain'
        },
        shards=4)
