from flaskdoc.swagger import base


class ExternalDocumentation(base.SwaggerBase):

  def __init__(self, url, description=None):
    super(ExternalDocumentation, self).__init__()
    self.url = url
    self.description = description

  def as_dict(self):
    d = base.SwaggerDict()
    d["name"] = self.url
    d["description"] = self.description
    d.update(super(ExternalDocumentation, self).as_dict())
    return d
