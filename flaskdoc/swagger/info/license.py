from flaskdoc.swagger.core import SwaggerBase


class License(SwaggerBase):
    """ License information for the exposed API. """

    def __init__(self, name, url=None):
        super(License, self).__init__()
        self.url = url
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, License):
            return False
        return self.name == other.name and self.url == other.url and self._extensions == other._extensions

    def __hash__(self):
        return hash((self.url, self.name, self._extensions))
