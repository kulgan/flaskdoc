import enum
import operations
from flaskdoc.swagger.core import SwaggerBase, SwaggerDict
from flaskdoc.swagger.parameters import QueryParameter
from flaskdoc.swagger.server import Server


class HttpMethod(enum.Enum):
    DELETE = "DELETE"
    HEAD = "HEAD"
    GET = "GET"
    OPTIONS = "OPTIONS"
    PATCH = "patch"
    POST = "POST"
    PUT = "PUT"
    TRACE = "TRACE"


class Paths(SwaggerBase):
    """
    Holds the relative paths to the individual endpoints and their operations. The path is appended to the URL
    from the Server Object in order to construct the full URL. The Paths MAY be empty, due to ACL constraints.
    """

    def __init__(self):
        super(Paths, self).__init__()
        self.items = SwaggerDict()

    def __iter__(self):
        for relative_url in self.items:
            yield relative_url

    def add_path_item(self, relative_url, path_item):
        """
        Adds a path item
        Args:
          relative_url (str): path url name, eg `/echo`
          path_item (PathItem|SwaggerDict) : PathItem instance describing the path
        """

        if isinstance(path_item, PathItem):
            path_item = path_item.as_dict()

        if not self.items:
            self.items = SwaggerDict()
        self.items[relative_url] = path_item

    def path_item(self, relative_url):
        return self.items.get(relative_url)

    def as_dict(self):
        return self.items or {}


class PathItem(SwaggerBase):
    """
    Describes the operations available on a single path. A Path Item MAY be empty, due to ACL constraints. The
    path itself is still exposed to the documentation viewer but they will not know which operations and parameters
    are available.
    """

    def __init__(self, ref=None, summary=None, description=None, parameters=None, servers=None):
        super(PathItem, self).__init__()

        self.ref = ref
        self.summary = summary
        self.description = description

        self.servers = servers
        self.parameters = parameters

        self.get = None  # type -> Operation
        self.delete = None  # type -> Operation
        self.head = None  # type -> Operation
        self.options = None  # type -> Operation
        self.patch = None  # type -> Operation
        self.post = None  # type -> Operation
        self.put = None  # type -> Operation
        self.trace = None  # type -> Operation

    def add_operation(self, operation):
        """
        Adds an operation
        Args:
          operation (swagger.path.operations.Operation): operation to add
        """
        http_method = operation.http_method.value.lower()
        setattr(self, http_method, operation)

    def add_server(self, server):
        """
        Adds an alternative server to service all operations in this path.

        Args:
            server (swagger.server.Serverr): alternative server to add
        """
        self.servers.add(server)

    def add_parameter(self, parameter):
        self.parameters.add(parameter)

    def merge_path_item(self, path_item):
        """
        Merges another path item into this on
        Args:
            path_item (PathItem): PathItem instance to merge
        """
        for server in path_item.servers:
            self.add_server(server)

        for param in path_item.parameters:
            self.add_parameter(param)

        self.get = path_item.get or self.get
        self.post = path_item.post or self.post
        self.put = path_item.put or self.put
        self.delete = path_item.delete or self.delete
        self.head = path_item.head or self.head
        self.trace = path_item.trace or self.trace
        self.patch = path_item.patch or self.patch
        self.options = path_item.options or self.options


class Callback(PathItem):
    """
    A map of possible out-of band callbacks related to the parent operation. Each value in the map is a Path Item
    Object that describes a set of requests that may be initiated by the API provider and the expected responses. The
    key value used to identify the callback object is an expression, evaluated at runtime, that identifies a URL to
    use for the callback operation.
    """


if __name__ == '__main__':
    pi = PathItem(ref="hello", summary="Summarixe this")
    s1 = Server(description="Server Man", url="https://dd.web.com")
    pi.add_server(s1)

    get = operations.GET(tags=["test"], summary="Yinyi de no sou", description="Kemi mi")
    get.operation_id = "getByExample"
    pr = QueryParameter(name="age", description="Just some shit")
    get.add_parameter(pr)
    pi.get = get
    ps = Paths()
    ps.add_path_item("/echo", pi)
    # print(ps)

    h = HttpMethod("GETs")
    print(h)