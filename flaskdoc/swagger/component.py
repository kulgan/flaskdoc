from flaskdoc.swagger.core import SwaggerBase, SwaggerDict


class Component(SwaggerBase):
    """
    Holds a set of reusable objects for different aspects of the OAS. All objects defined within the components
    object will have no effect on the API unless they are explicitly referenced from properties outside the
    components object.
    """

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
        d["parameters"] = self.parameters
        d["examples"] = self.examples
        d["requestBodies"] = self.request_bodies
        d["headers"] = self.headers
        d["securitySchemes"] = self.security_schemes
        d["links"] = self.links
        d["callbacks"] = self.callbacks

        d.update(super(Component, self).as_dict())
        return d
