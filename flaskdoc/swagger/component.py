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

    def add_schema(self, schema_name, schema):
        self.schemas[schema_name] = schema.as_dict()

    def add_response(self, response_name, response):
        self.responses[response_name] = response.as_dict()
