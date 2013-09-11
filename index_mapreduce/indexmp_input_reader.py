"""File contains input reader implementation."""

__author__ = 'rohit0286@gmail.com (Rohit Sharma).'

from mapreduce import input_readers
import models


class FeedsInputReader(input_readers.InputReader):
  """Class for index map reduce input readers."""

  def __init__(self, offset=0, limit=None):
    self.offset = offset
    self.limit = limit

  def __iter__(self):
    self._iter = FeedsInputReader._GetDatastoreObjects(
        self.offset, self.limit)
    return self

  def next(self):
    for data_object in self._iter:
      yield data_object

  def to_json(self):
    return {'offset': self.offset,
            'limit': self.limit}

  @classmethod
  def from_json(cls, input_shard_state):
    return cls(offset=input_shard_state.get('offset'),
               limit=input_shard_state.get('limit'))

  @classmethod
  def _GetDatastoreObjects(cls, db_offset, db_limit):
    feeds = models.Feed.GetAllFeeds().fetch(
        offset=db_offset, limit=db_limit)
    return feeds

  @classmethod
  def split_input(cls, mapper_spec):
    feeds = models.Feed.GetAllFeeds()
    number_of_feeds = feeds.count()
    shard_count = mapper_spec.shard_count
    split_points = cls._GetSplitPoints(number_of_feeds,
                                       shard_count)
    return [cls(offset=o, limit=l) for o,l in split_points]

  @classmethod
  def _GetSplitPoints(cls, number_of_feeds, shard_count):
    batch_size = None
    split_points = []
    if number_of_feeds > shard_count:
      batch_size = round(
          number_of_feeds / float(shard_count))
      current_offset = 0
      for offset in xrange(shard_count):
        if offset == shard_count:
          split_points.append((current_offset,
                               None))
        else:
          split_points.append((current_offset,
                               batch_size))
          current_offset += batch_size
    return split_points
