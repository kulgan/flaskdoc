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

    @staticmethod
    def camel_case(snake_case):
        cpnts = snake_case.split("_")
        return cpnts[0] + ''.join(x.title() for x in cpnts[1:])

    def as_dict(self):
        d = SwaggerDict()
        for key, val in vars(self).items():
            # skip extensions
            if key == "_extensions":
                continue

            if key.startswith("_"):
                key = key[1:]
                val = getattr(self, key, None)

            # map ref
            if key == "ref":
                key = "$ref"

            if isinstance(val, SwaggerBase):
                val = val.as_dict()

            if isinstance(val, (set, list)):
                val = [v.as_dict() if isinstance(v, SwaggerBase) else v for v in val]

            d[self.camel_case(key)] = val

        if self._extensions:
            d.update(self._extensions)
        return d

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

        self.openapi = open_api_version
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

    def add_paths(self, paths):
        """
        Updates paths to include all paths in `paths`
        Args:
            paths:

        Returns:

        """
        for r_url in paths:
            self.paths.add_path_item(r_url, paths.path_item(r_url))


class SwaggerDict(OrderedDict):

    def __setitem__(self, key, value):
        if value not in [False, True] and not value:
            return
        super(SwaggerDict, self).__setitem__(key, value)
