from flaskdoc.swagger.core import SwaggerBase, SwaggerDict
from flaskdoc.swagger.external import ExternalDocumentation


class Tag(SwaggerBase):

    def __init__(self, name, description=None, external_doc=None):
        super(Tag, self).__init__()
        self.name = name
        self.description = description
        self._external_doc = external_doc  # type ExternalDocumentation

    def external_doc(self, url, description=None):
        self._external_doc = ExternalDocumentation(url=url, description=description)

    def as_dict(self):
        d = SwaggerDict()
        d["name"] = self.name
        if self._external_doc:
            d["description"] = self._external_doc.as_dict()
        d.update(super(Tag, self).as_dict())
        return d
