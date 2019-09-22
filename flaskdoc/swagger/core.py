import json

from collections import OrderedDict


class SwaggerBase(object):

    def __init__(self):
        self._extensions = None

    def add_extension(self, name, value):
        """
        Allows extensions to the Swagger Schema. The field name MUST begin with x-,
        for example, x-internal-id. The value can be null, a primitive, an array or an object.
        Args:
            name (str): custom extension name, must begin with x-
            value (Any): value, can be None, any object or list
        Returns:
            SwaggerBase: for chaining
        Raises:
            ValueError: if key name is invalid
        """

        self.validate_extension_name(name)

        if not self._extensions:
            self._extensions = SwaggerDict()
        self._extensions[name] = value
        return self

    @staticmethod
    def validate_extension_name(name):
        """
        Validates a custom extension name
        Args:
            name (str): custom extension name
        Raises:
            ValueError: if key name is invalid
        """
        if not (name and name.startswith("x-")):
            raise ValueError("Custom extension must start with x-")

    def as_dict(self):
        return self._extensions or {}

    def __repr__(self):
        return json.dumps(self.as_dict(), indent=2)


class OpenApi(SwaggerBase):
    """ This is the root document object of the OpenAPI document. """

    def __init__(self, info, paths, open_api_version="3.0.2"):
        """
        OpenApi specs tree, contains the overall specs for the API
        Args:
            open_api_version (str): Open API version used by API
            info (flaskdoc.swagger.info.Info): open api info object
            paths (flaskdoc.swagger.path.Paths): Paths definitions
        """
        super(OpenApi, self).__init__()

        self.open_api = open_api_version
        self.info = info

        # TODO disallow duplicates
        self.tags = []  # type -> swagger.tag.Tag
        self.paths = paths  # type -> swagger.path.Paths
        self.servers = set()

        self.components = None
        self.security = []

        self.external_docs = None

    def add_tag(self, tag):
        """
        Adds a tag to the top level spec
        Args:
            tag (swagger.tag.Tag): tag to add
        """
        self.tags.append(tag)

    def add_server(self, server):
        self.servers.add(server)

    def as_dict(self):
        d = SwaggerDict()
        d["openapi"] = self.open_api
        d["info"] = self.info.as_dict()
        d["servers"] = [s.as_dict() for s in self.servers] if self.servers else None
        d["paths"] = self.paths.as_dict()
        d["components"] = self.components
        d["security"] = [s.as_dict() for s in self.security] if self.security else None
        d["tags"] = [tag.as_dict() for tag in self.tags] if self.tags else None
        d["externalDocs"] = self.external_docs

        d.update(super(OpenApi, self).as_dict())
        return d


class SwaggerDict(OrderedDict):

    def __setitem__(self, key, value):
        if value not in [False, True] and not value:
            return
        super(SwaggerDict, self).__setitem__(key, value)
