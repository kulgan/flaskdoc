from flaskdoc.swagger.core import SwaggerBase, SwaggerDict


class Component(SwaggerBase):

    def __init__(self):
        super(Component, self).__init__()
        self.schemas = {}
        self.responses = {}
        self.parameters = {}
        self.examples = {}
        self.request_bodies = {}
        self.headers = {}
        self.security_schemes = {}
        self.links = {}
        self.callbacks = {}

    def as_dict(self):
        d = SwaggerDict()
        d["schemas"] = self.schemas
        d["responses"] = self.responses

        d.update(super(Component, self).as_dict())
        return d
