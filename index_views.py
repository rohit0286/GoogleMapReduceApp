"""File contains handlers for feeds."""

__author__ = 'rohit0286@gmail.com (Rohit Sharma).'

import webapp2
from index_mapreduce import index

class FeedsIndexer(webapp2.RequestHandler):
  """Contains handlers for saving and rendering feeds."""

  def get(self):
    """Initiates Map Reduce for indexing Feeds."""
    pipeline = index.IndexPipeline()
    pipeline.start()
    self.redirect('{0}/status?root={1}'.format(
        pipeline.base_path, pipeline.pipeline_id))
