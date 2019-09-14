import collections

from flaskdoc.swagger.base import SwaggerBase
from swagger.external import ExternalDocumentation


class Tag(SwaggerBase):

  def __init__(self, name, description=None, external_doc=None):
    super(Tag, self).__init__()
    self.name = name
    self.description = description
    self.external_doc = external_doc  # type ExternalDocumentation

  def external_doc(self, url, description=None):
    self.external_doc = ExternalDocumentation(url=url, description=description)

  def as_dict(self):
    d = super(Tag, self).as_dict()
    d.update(collections.OrderedDict(
      name=self.name,
      description=self.external_doc.as_dict()
    ))
    return d
