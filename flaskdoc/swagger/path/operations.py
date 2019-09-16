from flaskdoc.swagger.core import SwaggerBase, SwaggerDict
from flaskdoc.swagger.path import paths


class Operation(SwaggerBase):

    def __init__(self, responses="200", tags=None, summary=None,
                 description=None, operations_id=None, parameters=None):
        super(Operation, self).__init__()
        self.responses = responses
        self.tags = tags or []  # type -> List[str]
        self.summary = summary
        self.description = description
        self.operation_id = operations_id

        self.deprecated = False
        self.parameters = parameters or []

    @property
    def http_method(self):
        return None

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    @staticmethod
    def from_op(http_method):
        if http_method == paths.HttpMethod.GET:
            return GET()
        return None

    def as_dict(self):
        d = SwaggerDict()
        d["tags"] = self.tags
        d["summary"] = self.summary
        d["description"] = self.description
        d["parameters"] = [p.as_dict() for p in self.parameters]
        d.update(super(Operation, self).as_dict())
        return d


class GET(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.GET


class POST(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.POST


class PUT(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.PUT


class HEAD(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.HEAD


class OPTIONS(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.OPTIONS


class PATCH(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.PATCH


class TRACE(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.TRACE
