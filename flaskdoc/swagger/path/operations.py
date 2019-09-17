from flaskdoc.swagger.core import SwaggerBase, SwaggerDict
from flaskdoc.swagger.path import paths


class Operation(SwaggerBase):

    def __init__(self, tags=None, summary=None,
                 description=None, operations_id=None):
        super(Operation, self).__init__()
        self.tags = tags or []  # type -> List[str]
        self.summary = summary
        self.description = description
        self.external_docs = None
        self.operation_id = operations_id
        self.parameters = []
        self.request_body = None
        self.responses = None
        self.callbacks = {}
        self.deprecated = False
        self.security = []
        self.servers = set()

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
        d["externalDocs"] = self.external_docs.as_dict() if self.external_docs else None
        d["operationId"] = self.operation_id
        d["parameters"] = [p.as_dict() for p in self.parameters] if self.parameters else []
        d["requestBody"] = self.request_body.as_dict() if self.request_body else None
        d["responses"] = self.responses.as_dict() if self.responses else None
        d["callbacks"] = {k: v.as_dict() for k,v in self.callbacks.items()}
        d["deprecated"] = self.deprecated
        d["security"] = [s.as_dict() for s in self.security]
        d["servers"] = [s.as_dict() for s in self.servers]
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
