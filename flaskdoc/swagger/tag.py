from flaskdoc.swagger.core import SwaggerBase, SwaggerDict
from flaskdoc.swagger.media import ExternalDocumentation


class Tag(SwaggerBase):

    def __init__(self, name, description=None, external_doc=None):
        super(Tag, self).__init__()
        self.name = name
        self.description = description
        self._external_docs = external_doc  # type ExternalDocumentation

    def external_docs(self, url, description=None):
        self._external_docs = ExternalDocumentation(url=url, description=description)
