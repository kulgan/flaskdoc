from flaskdoc.swagger.core import SwaggerBase, SwaggerDict


class ExternalDocumentation(SwaggerBase):
    """ Allows referencing an external resource for extended documentation. """

    def __init__(self, url, description=None):
        super(ExternalDocumentation, self).__init__()
        self.url = url
        self.description = description

    def as_dict(self):
        d = SwaggerDict()
        d["url"] = self.url
        d["description"] = self.description
        d.update(super(ExternalDocumentation, self).as_dict())
        return d
