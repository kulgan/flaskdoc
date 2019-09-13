from flaskdoc.swagger.base import SwaggerBase


class Tag(SwaggerBase):

    def __init__(self, name, description=None, external_docs=None):

        super(Tag, self).__init__()
        self.name = name
        self.description = description
        self.external_docs = external_docs
