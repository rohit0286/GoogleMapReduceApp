"""File contains handlers for warmup requests."""

__author__ = 'rohit0286@gmail.com (Rohit Sharma).'

import json
import models
import os
import settings
import webapp2


class Warmup(webapp2.RequestHandler):
  """Class to handler for warmup request."""

  def get(self):
    """Save RSS source in db."""
    json_data = self._GetJson()
    for rss_source in json_data.get('rss-sources'):
      source_name = rss_source.get('name')
      rss_source_db = models.RSSSource.GetSourceByName(
          source_name)
      if rss_source_db:
        rss_source_db.UpdateSource(rss_source)
      else:
        models.RSSSource.AddSource(rss_source)

  def _GetJson(self):
    """Gets RSS sources json from a JSON file."""
    json_file = os.path.join(os.path.dirname(__file__),
                             settings.RSS_SOURCES_JSON_FILE)
    with open(json_file) as json_file_data:
      json_data = json.load(json_file_data)
    return json_data
