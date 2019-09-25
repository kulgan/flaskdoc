from flaskdoc.swagger.core import SwaggerBase, SwaggerDict
from flaskdoc.swagger.media import Content


class ResponsesObject(SwaggerBase):
    """
    A container for the expected responses of an operation. The container maps a HTTP response code to the
    expected response. The documentation is not necessarily expected to cover all possible HTTP response codes
    because they may not be known in advance. However, documentation is expected to cover a successful operation
    response and any known errors. The default MAY be used as a default response object for all HTTP codes that are
    not covered individually by the specification. The Responses Object MUST contain at least one response code,
    and it SHOULD be the response for a successful operation call.
    """

    def __init__(self, default=None):
        super(ResponsesObject, self).__init__()
        self.default = default
        self.responses = {}

    def add_response(self, status_code, response):
        self.responses[status_code] = response

    def as_dict(self):
        d = SwaggerDict()
        d["default"] = self.default.as_dict() if self.default else None
        for code, response in self.responses.items():
            d[code] = response.as_dict() if response else None
        # d.update(super(ResponsesObject, self).as_dict())

        return d


class ResponseObject(SwaggerBase):
    """
    Describes a single response from an API Operation, including design-time, static links to operations based on
    the response.
    """

    def __init__(self, description):
        super(ResponseObject, self).__init__()
        self.description = description
        self.headers = {}
        self.content = None
        self.links = None

    def add_header(self, name, header):
        self.headers[name] = header

    def add_content(self, media_type, content):
        if not self.content:
            self.content = Content()
        self.content.add_media_type(media_type, content)

    def add_linik(self, link_name, link):
        pass
