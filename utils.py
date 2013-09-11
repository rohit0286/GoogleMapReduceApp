"""Contains utility methods."""

__author__ = 'rohit0286@gmail.com (Rohit Sharma).'


import os
import settings
import time
from google.appengine.ext.webapp.template import render


def RenderTemplate(template, response, payload=None):
  """Renders the template.
  Args:
    template: File name of template.
    response: Http Response.
    payload: payload to use while rendering template.
  """

  template_file_path = '{0}/{1}'.format(
      settings.TEMPLATES_FOLDER, template)
  tmpl = os.path.join(os.path.dirname(__file__),
                      template_file_path)
  response.out.write(render(tmpl, payload))