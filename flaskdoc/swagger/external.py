import collections

from flaskdoc.swagger.base import SwaggerBase


class ExternalDocumentation(SwaggerBase):

  def __init__(self, url, description=None):
    super(ExternalDocumentation, self).__init__()
    self.url = url
    self.description = description

  def as_dict(self):
    d = super(ExternalDocumentation, self).as_dict()
    d.update(collections.OrderedDict(
      name=self.url,
      description=self.description
    ))
    return d
