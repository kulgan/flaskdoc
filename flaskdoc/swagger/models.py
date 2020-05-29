import enum
import json
import logging
from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum
from typing import List, Any, Set, Union, Dict

from flaskdoc.pallets.plugins import register_spec

logger = logging.getLogger(__name__)


class SwaggerDict(OrderedDict):

    def __setitem__(self, key, value):
        if value not in [False, True] and not value:
            return
        super(SwaggerDict, self).__setitem__(key, value)


class ApiDecoratorMixin(object):
    """ Makes a model a decorator that registers itself """

    def __call__(self, func):
        register_spec(func, self)
        return func


class ModelMixin(object):
    """ Model mixin that provides common functionalities like to dict and to json """

    @staticmethod
    def camel_case(snake_case):
        cpnts = snake_case.split("_")
        return cpnts[0] + ''.join(x.title() for x in cpnts[1:])

    def dict(self):
        d = SwaggerDict()
        for key, val in vars(self).items():
            # skip extensions
            if key == "extensions":
                continue

            if key.startswith("_"):
                key = key[1:]
                val = getattr(self, "q_" + key, None)

            # map ref
            if key == "ref":
                key = "$ref"

            if isinstance(val, ModelMixin) or hasattr(val, "dict"):
                val = val.dict()

            if isinstance(val, (set, list)):
                val = [v.dict() if isinstance(v, ModelMixin) else v for v in val]

            if isinstance(val, dict):
                val = {k: v.dict() if isinstance(v, ModelMixin) else v for k, v in val.items()}

            d[self.camel_case(key)] = val

        return d

    def json(self, indent=2):
        return json.dumps(self.dict(), indent=indent)

    def __repr__(self):
        return self.json(indent=2)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for field, val in vars(self).items():
            if val != getattr(other, field, None):
                return False
        return True

    def __hash__(self):
        return hash((val for _, val in vars(self).items()))


class ExtensionMixin(ModelMixin):

    extensions: Dict[str, Any] = None

    def add_extension(self, name, value):
        """
        Allows extensions to the Swagger Schema. The field name MUST begin with x-,
        for example, x-internal-id. The value can be null, a primitive, an array or an object.
        Args:
            name (str): custom extension name, must begin with x-
            value (Any): value, can be None, any object or list
        Returns:
            ModelMixin: for chaining
        Raises:
            ValueError: if key name is invalid
        """

        self.validate_extension_name(name)

        if not self.extensions:
            self.extensions = SwaggerDict()
        self.extensions[name] = value
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

    def dict(self):
        di = super(ExtensionMixin, self).dict()
        if self.extensions:
            di.update(self.extensions)
        return di


class ContainerModel(ModelMixin):

    items = None

    def add(self, key, item):
        """ Adds an item
        Args:
            key (str): item key
            item (dict): item
        """
        if self.items is None:
            self.items = SwaggerDict()
        self.items[key] = item

    def get(self, key):
        if self.items is None:
            self.items = SwaggerDict()
        return self.items.get(key)

    def __iter__(self):
        for item in self.items:
            yield item

    def dict(self):
        return self.items

    def json(self, indent=2):
        return json.dumps(self.items, indent=indent)

    def __repr__(self):
        return self.json(indent=2)


@dataclass
class License(ExtensionMixin):
    """ License information for the exposed API. """

    name: str
    url: str = None


@dataclass
class Contact(ExtensionMixin):
    """ Contact information for the exposed API. """

    name: str = None
    email: str = None
    url: str = None


@dataclass
class Info(ExtensionMixin):
    """
    The object provides metadata about the API. The metadata MAY be used by the clients if needed, and MAY be
    presented in editing or documentation generation tools for convenience.
    """
    title: str
    version: str
    description: str = None
    terms_of_service: str = None
    contact: Contact = None
    license: License = None


@dataclass
class ServerVariable(ExtensionMixin):
    """ An object representing a Server Variable for server URL template substitution.
        An object representing a server variable

        Attributes:
            default (str): REQUIRED. The default value to use for substitution, which SHALL be sent if an alternate
                                value is not supplied. Note this behavior is different than the Schema Object's
                                treatment of default values, because in those cases parameter values are optional.
            enum (List[str]): An enumeration of string values to be used if the substitution options are
                                from a limited set
            description (str): An optional description for the server variable. CommonMark syntax MAY
                                be used for rich text representation.
        """

    default: str
    enum: List[str] = None
    description: str = None


@dataclass
class Server(ExtensionMixin):
    """ An object representing a Server. """

    url: str
    description: str = None
    variables: Dict[str, ServerVariable] = None

    def add_variable(self, name, variable):
        """
        Adds a server variable
        Args:
            name (str): variable name
            variable (ServerVariable|dict): Server variable instance
        """
        if self.variables is None:
            self.variables = SwaggerDict()
        self.variables[name] = variable.dict()


class Style(Enum):
    """ Style values defined to aid serializing different simple parameters """

    FORM = "form"
    LABEL = "label"
    MATRIX = "matrix"
    SIMPLE = "simple"
    SPACE_DELIMITED = "spaceDelimited"
    PIPE_DELIMITED = "pipeDelimited"
    DEEP_OBJECT = "deepObject"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


@dataclass
class ReferenceObject(ModelMixin):

    ref: str


@dataclass
class Discriminator(ModelMixin):
    """ When request bodies or response payloads may be one of a number of different schemas, a discriminator object
    can be used to aid in serialization, deserialization, and validation. The discriminator is a specific object in a
    schema which is used to inform the consumer of the specification of an alternative schema based on the value
    associated with it. """

    property_name: str
    mapping: Dict[str, str] = None


@dataclass
class XML(ExtensionMixin):
    """ A metadata object that allows for more fine-tuned XML model definitions. When using arrays, XML element names
    are not inferred (for singular/plural forms) and the name property SHOULD be used to add that information. See
    examples for expected behavior.
    """

    name: str = None
    namespace: str = None
    prefix: str = None
    attribute: bool = False
    wrapped: bool = False


@dataclass
class ExternalDocumentation(ExtensionMixin):
    """ Allows referencing an external resource for extended documentation. """

    url: str
    description: str = None


@dataclass
class Encoding(ExtensionMixin):
    """ A single encoding definition applied to a single schema property. """

    content_type: str
    headers: Dict[str, Union[ReferenceObject]] = None
    style: Style = None
    explode: bool = True
    allow_reserved: bool = False

    def add_header(self, name, header):
        if not self.headers:
            self.headers = SwaggerDict()
        self.headers[name] = header


@dataclass
class Example(ExtensionMixin):

    summary: str = None
    description: str = None
    value: Any = None
    external_value: str = None


@dataclass
class Schema(ModelMixin):

    ref: str = None
    title: str = None
    multiple_of = None
    maximum = None
    exclusive_maximum = None
    minimum = None
    exclusive_minimum = None
    max_length = None  # type: int
    min_length = None  # type: int
    pattern = None
    max_items = None  # type: ignore
    min_items = None  # type: ignore
    unique_item = None
    max_properties = None  # type: ignore
    min_properties = None  # type: ignore
    required = None
    enum = None
    type: str = None
    all_of = None
    one_of = None
    any_of = None
    _not = None  # type: ignore
    items = None
    properties = None
    additional_properties = None
    description = None
    format: str = None
    default = None
    nullable = None
    discriminator = None
    read_only = None
    write_only = None
    xml = None
    external_docs = None
    example = None
    deprecated = None

    def q_not(self):
        return self._not


@dataclass
class MediaType(ModelMixin):
    """ Each Media Type Object provides schema and examples for the media type identified by its key. """

    schema: Union[ReferenceObject, Schema] = None
    example: Any = None
    examples: Dict[str, Union[Example, ReferenceObject]] = None
    encoding: Dict[str, Encoding] = None

    def add_example(self, name: str, example: Union[Example, ReferenceObject]):
        if self.examples is None:
            self.examples = SwaggerDict()
        self.examples[name] = example

    def add_encoding(self, name: str, encoding: Encoding):
        if self.encoding is None:
            self.encoding = SwaggerDict()
        self.encoding[name] = encoding


class Content(object):

    def __init__(self):
        super(Content, self).__init__()
        self.contents = SwaggerDict()

    def add_media_type(self, name: str, media_type: MediaType):
        self.contents[name] = media_type.dict()

    def dict(self):
        return self.contents


@dataclass
class RequestBody(ExtensionMixin):

    # FIXME: reuse Content Class ?
    content: Dict[str, MediaType]
    description: str = None
    required: bool = False


class Component(ExtensionMixin):
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
        self.schemas[schema_name] = schema.dict()

    def add_response(self, response_name, response):
        self.responses[response_name] = response.dict()


class RelativePath(object):

    def __init__(self, url):
        self.len = 0
        self.params = {}
        self.url = url

        self.parse(url)

    def parse(self, url_template):
        """
        Extracts positional parameters from url
        Args:
            url_template:

        Returns:

        """
        url_paths = url_template.split("/")

        self.len = len(url_paths)
        for i in range(self.len):
            path = url_paths[i]
            if path.startswith("{") and path.endswith("}"):
                self.params[i] = path.replace("{", "").replace("}", "")


class ParameterLocation(Enum):
    COOKIE = "cookie"
    HEADER = "header"
    PATH = "path"
    QUERY = "query"

    def __repr__(self):
        return self.value


@dataclass
class Parameter(ModelMixin, ApiDecoratorMixin):
    """
    Describes a single operation parameter.
    A unique parameter is defined by a combination of a name and location.
    """

    name: str
    _in: ParameterLocation = None
    required: bool = False
    description: str = None
    deprecated: bool = False

    allow_empty_value: bool = False
    allow_reserved: bool = False
    schema: Union[Schema, ReferenceObject] = None
    content: Dict[str, MediaType] = None

    explode: bool = False
    _style: Style = None

    example: Any = None
    examples: Dict[str, Union[Example, ReferenceObject]] = None

    @property
    def q_in(self):
        return self._in.value

    @property
    def q_style(self):
        return self._style.value


@dataclass
class PathParameter(Parameter):

    _in: ParameterLocation = ParameterLocation.PATH
    required: bool = True
    _style: Style = Style.SIMPLE


@dataclass
class QueryParameter(Parameter):

    _in: ParameterLocation = ParameterLocation.QUERY
    _style: Style = Style.FORM


@dataclass
class HeaderParameter(Parameter):

    _in: ParameterLocation = ParameterLocation.HEADER
    _style: Style = Style.SIMPLE


@dataclass
class CookieParameter(Parameter):

    _in: ParameterLocation = ParameterLocation.COOKIE
    _style: Style = Style.FORM


@dataclass
class Link(ExtensionMixin):
    """
    The Link object represents a possible design-time link for a response. The presence of a link does not guarantee
    the caller's ability to successfully invoke it, rather it provides a known relationship and traversal mechanism
    between responses and other operations. Unlike dynamic links (i.e. links provided in the response payload),
    the OAS linking mechanism does not require link information in the runtime response. For computing links,
    and providing instructions to execute them, a runtime expression is used for accessing values in an operation and
    using them as parameters while invoking the linked operation.
    """

    operation_ref: str = None
    operation_id: str = None
    description: str = None
    parameters: Dict[str, Any] = None
    request_body: Any = None
    server: Server = None


@dataclass
class ResponseObject(ExtensionMixin):
    """
    Describes a single response from an API Operation, including design-time, static links to operations based on
    the response.
    """

    description: str
    content: Dict[str, MediaType] = None
    headers: Dict[str, Union[ReferenceObject, HeaderParameter]] = None
    links: Dict[str, Union[Link, ReferenceObject]] = None

    def add_header(self, name: str, header: Union[ReferenceObject, HeaderParameter]):
        if self.headers is None:
            self.headers = SwaggerDict()
        self.headers[name] = header

    def add_content(self, media_type: str, content: MediaType):
        if not self.content:
            self.content = SwaggerDict()
        self.content[media_type] = content

    def add_link(self, link_name: str, link: Union[Link, ReferenceObject]):
        if self.links is None:
            self.links = SwaggerDict()
        self.links[link_name] = link


@dataclass
class ResponsesObject(ExtensionMixin):
    """
    A container for the expected responses of an operation. The container maps a HTTP response code to the
    expected response. The documentation is not necessarily expected to cover all possible HTTP response codes
    because they may not be known in advance. However, documentation is expected to cover a successful operation
    response and any known errors. The default MAY be used as a default response object for all HTTP codes that are
    not covered individually by the specification. The Responses Object MUST contain at least one response code,
    and it SHOULD be the response for a successful operation call.
    """

    default: ResponseObject = None
    responses: Dict[str, ResponseObject] = None

    def add_response(self, status_code: str, response: ResponseObject):
        if self.responses is None:
            self.responses = SwaggerDict()
        self.responses[status_code] = response


@dataclass
class Tag(ModelMixin, ApiDecoratorMixin):

    name: str
    description: str = None
    external_docs: ExternalDocumentation = None

    def external_doc(self, url, description=None):
        self.external_docs = ExternalDocumentation(url=url, description=description)


@dataclass
class Operation(ExtensionMixin, ApiDecoratorMixin):
    """ Describes a single API operation on a path. """

    responses: ResponsesObject
    tags: List[str] = None
    summary: str = None
    description: str = None
    external_docs: ExternalDocumentation = None
    operation_id: str = None
    parameters: List[Union[ReferenceObject, Parameter]] = None
    request_body: Union[RequestBody, ReferenceObject] = None
    callbacks: Dict[str, ReferenceObject] = None
    deprecated = False
    security: List[Dict[str, Any]] = None
    servers: Set[Server] = None

    @property
    def http_method(self):
        return None

    def add_parameter(self, parameter: Union[Parameter, ReferenceObject]):
        if self.parameters is None:
            self.parameters = []
        self.parameters.append(parameter)

    @staticmethod
    def from_op(http_method: str, responses: ResponsesObject):
        """ Factory for creating instances of Http Operations """

        http_method = HttpMethod(http_method)
        if http_method == HttpMethod.GET:
            return GET(responses=responses)
        elif http_method == HttpMethod.POST:
            return POST(responses=responses)
        elif http_method == HttpMethod.PUT:
            return PUT(responses=responses)
        elif http_method == HttpMethod.DELETE:
            return DELETE(responses=responses)
        elif http_method == HttpMethod.OPTIONS:
            return OPTIONS(responses=responses)
        elif http_method == HttpMethod.TRACE:
            return TRACE(responses=responses)
        elif http_method == HttpMethod.PATCH:
            return PATCH(responses=responses)
        elif http_method == HttpMethod.HEAD:
            return HEAD(responses=responses)


@dataclass
class PathItem(ModelMixin):
    """
    Describes the operations available on a single path. A Path Item MAY be empty, due to ACL constraints. The
    path itself is still exposed to the documentation viewer but they will not know which operations and parameters
    are available.
    """

    ref: str = None
    summary: str = None
    description: str = None

    servers: List[Server] = None
    parameters: List[Union[Parameter, ReferenceObject]] = None

    get: Operation = None
    delete: Operation = None
    head: Operation = None
    options: Operation = None
    patch: Operation = None
    post: Operation = None
    put: Operation = None
    trace: Operation = None

    def add_operation(self, operation):
        """
        Adds an operation
        Args:
          op
          ration (Operation): operation to add
          https://docs.google.com/document/d/1TYZMZnqVeBF0VVIkvGHdf0zVYYiJynue98psff_R9ys/edit?usp=sharinghttps://docs.google.com/document/d/1TYZMZnqVeBF0VVIkvGHdf0zVYYiJynue98psff_R9ys/edit?usp=sharing   tggr
        """
        http_method = operation.http_method.value.lower()
        setattr(self, http_method, operation)

    def add_server(self, server):
        """
        Adds an alternative server to service all operations in this path.

        Args:
            server (Server): alternative server to add
        """
        if not self.servers:
            self.servers = []
        self.servers.append(server)

    def add_parameter(self, parameter):
        if not self.parameters:
            self.parameters = []
        self.parameters.append(parameter)

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


class Paths(ContainerModel):
    """
    Holds the relative paths to the individual endpoints and their operations. The path is appended to the URL
    from the Server Object in order to construct the full URL. The Paths MAY be empty, due to ACL constraints.
    """

    def add(self, relative_url: str, path_item: Union[PathItem, SwaggerDict]):
        """
        Adds a path item
        Args:
          relative_url (str): path url name, eg `/echo`
          path_item (PathItem|SwaggerDict) : PathItem instance describing the path
        """

        if isinstance(path_item, PathItem):
            path_item = path_item.dict()
        super(Paths, self).add(relative_url, path_item)


@dataclass
class GET(Operation):

    @property
    def http_method(self):
        return HttpMethod.GET


@dataclass
class POST(Operation):

    @property
    def http_method(self):
        return HttpMethod.POST


class PUT(Operation):

    @property
    def http_method(self):
        return HttpMethod.PUT


class HEAD(Operation):

    @property
    def http_method(self):
        return HttpMethod.HEAD


class OPTIONS(Operation):

    @property
    def http_method(self):
        return HttpMethod.OPTIONS


class PATCH(Operation):

    @property
    def http_method(self):
        return HttpMethod.PATCH


class TRACE(Operation):

    @property
    def http_method(self):
        return HttpMethod.TRACE


class DELETE(Operation):

    @property
    def http_method(self):
        return HttpMethod.DELETE


class HttpMethod(enum.Enum):
    DELETE = "DELETE"
    HEAD = "HEAD"
    GET = "GET"
    OPTIONS = "OPTIONS"
    PATCH = "patch"
    POST = "POST"
    PUT = "PUT"
    TRACE = "TRACE"


@dataclass
class Callback(ModelMixin):
    """
    A map of possible out-of band callbacks related to the parent operation. Each value in the map is a Path Item
    Object that describes a set of requests that may be initiated by the API provider and the expected responses. The
    key value used to identify the callback object is an expression, evaluated at runtime, that identifies a URL to
    use for the callback operation.
    """

    expression: PathItem


class SecuritySchemeType(Enum):

    API_KEY = "apiKey"
    HTTP = "http"
    OAUTH2 = "oauth2"
    OPEN_ID_CONNECT = "openIdConnect"


class SecurityScheme(ExtensionMixin):
    """ Defines a security scheme that can be used by the operations. Supported schemes are HTTP authentication,
    an API key (either as a header or as a query parameter), OAuth2's common flows (implicit, password, application
    and access code) as defined in RFC6749, and OpenID Connect Discovery. """

    def __init__(self,
                 scheme_type,
                 name,
                 description=None,
                 scheme=None,
                 bearer_format=None,
                 flows=None,
                 open_id_connect_url=None):
        super(SecurityScheme, self).__init__()

        self.type = SecuritySchemeType(scheme_type) if isinstance(scheme_type, str) else scheme_type
        self.name = name  # type: str
        self.description = description  # type: str
        self.scheme = scheme  # type: str
        self.bearer_format = bearer_format  # type: str
        self.flows = flows
        self.open_id_connect_url = open_id_connect_url


class OAuthFlows(ExtensionMixin):
    """ Allows configuration of the supported OAuth Flows. """

    def __init__(self,
                 implicit=None,
                 password=None,
                 client_credentials=None,
                 authorization_code=None):
        super(OAuthFlows, self).__init__()

        self.implicit = implicit  # type: OAuthFlow
        self.password = password  # type: OAuthFlow
        self.client_credentials = client_credentials  # type: OAuthFlow
        self.authorization_code = authorization_code  # type: OAuthFlow


class OAuthFlow(ExtensionMixin):
    """ Configuration details for a supported OAuth Flow """

    def __init__(self,
                 authorization_url=None,
                 token_url=None,
                 refresh_url=None,
                 scopes=None):
        super(OAuthFlow, self).__init__()

        self.authorization_url = authorization_url  # type: str
        self.token_url = token_url  # type: str
        self.refresh_url = refresh_url  # type: str
        self.scopes = scopes  # type: dict


class OpenApi(ModelMixin):
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
            tag (swagger.Tag): tag to add
        """
        self.tags.append(tag)

    def add_server(self, server):
        self.servers.add(server)

    def add_paths(self, paths, url_prefix=None, blp_prefix=None):
        """
        Updates paths to include all paths in `paths`
        Args:
            paths:
            url_prefix (str): prefix
            blp_prefix (str): blueprint url prefix
        Returns:

        """
        url_prefix = url_prefix or ""
        blp_prefix = blp_prefix or ""
        for r_url in paths:
            path_url = "{}{}{}".format(url_prefix, blp_prefix, r_url)
            self.paths.add(path_url, paths.get(r_url))


if __name__ == '__main__':
    paths = Paths()
    paths.add("test", None)
