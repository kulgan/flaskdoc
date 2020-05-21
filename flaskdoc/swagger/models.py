import json
import logging

from collections import OrderedDict

import enum
from enum import Enum

logger = logging.getLogger(__name__)


class SwaggerDict(OrderedDict):

    def __setitem__(self, key, value):
        if value not in [False, True] and not value:
            return
        super(SwaggerDict, self).__setitem__(key, value)


class BaseModel(object):

    @staticmethod
    def camel_case(snake_case):
        cpnts = snake_case.split("_")
        return cpnts[0] + ''.join(x.title() for x in cpnts[1:])

    def dict(self):
        d = SwaggerDict()
        for key, val in vars(self).items():
            # skip extensions
            if key == "_extensions":
                continue

            if key.startswith("_"):
                key = key[1:]
                val = getattr(self, "q_" + key, None)

            # map ref
            if key == "ref":
                key = "$ref"

            if isinstance(val, BaseModel):
                val = val.dict()

            if isinstance(val, (set, list)):
                val = [v.dict() if isinstance(v, BaseModel) else v for v in val]

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


class ExtensionModel(BaseModel):

    def __init__(self):
        super(ExtensionModel, self).__init__()

        self._extensions = None

    def extensions(self):
        return self._extensions

    def add_extension(self, name, value):
        """
        Allows extensions to the Swagger Schema. The field name MUST begin with x-,
        for example, x-internal-id. The value can be null, a primitive, an array or an object.
        Args:
            name (str): custom extension name, must begin with x-
            value (Any): value, can be None, any object or list
        Returns:
            BaseModel: for chaining
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

    def dict(self):
        di = super(ExtensionModel, self).dict()
        if self._extensions:
            di.update(self._extensions)
        return di


class ContainerModel(object):

    def __init__(self):
        self.items = SwaggerDict()

    def add(self, key, item):
        """
        Adds an item
        Args:
            key (str): item key
            item (dict): item
        """
        self.items[key] = item

    def get(self, key):
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


class License(ExtensionModel):
    """ License information for the exposed API. """

    def __init__(self, name, url=None):
        super(License, self).__init__()

        self.url = url
        self.name = name


class Contact(ExtensionModel):
    """ Contact information for the exposed API. """

    def __init__(self, name=None, url=None, email=None):
        super(Contact, self).__init__()

        self.name = name
        self.email = email
        self.url = url


class Info(ExtensionModel):
    """
    The object provides metadata about the API. The metadata MAY be used by the clients if needed, and MAY be
    presented in editing or documentation generation tools for convenience.
    """

    def __init__(self, title, version, description=None, terms_of_service=None,
                 contact=None, license=None):
        """
        API metadata object
        Args:
            title (str): the title of the application (required)
            version (str): API version (required)
            description (str): short description of the application
            terms_of_service (str): API terms of service
            contact (flaskdoc.swagger.info.Contact): API contact information
            license (flaskdoc.swagger.info.License): API license information
        """
        super(Info, self).__init__()

        self.title = title
        self.description = description
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license = license
        self.version = version


class Server(ExtensionModel):
    """ An object representing a Server. """

    def __init__(self, url, description=None, variables=None):
        super(Server, self).__init__()

        self.url = url
        self.description = description
        self.variables = variables or SwaggerDict()

    def add_variable(self, name, variable):
        """
        Adds a server variable
        Args:
            name (str): variable name
            variable (ServerVariable|dict): Server variable instance
        """
        self.variables[name] = variable.dict()


class ServerVariable(ExtensionModel):
    """ An object representing a Server Variable for server URL template substitution. """

    def __init__(self, default_val, enum_values=None, description=None):
        """
        An object representing a server variable
        Args:
            default_val (str): REQUIRED. The default value to use for substitution, which SHALL be sent if an alternate
                                value is not supplied. Note this behavior is different than the Schema Object's
                                treatment of default values, because in those cases parameter values are optional.
            enum_values (str|List[str]): An enumeration of string values to be used if the substitution options are
                                from a limited set
            description (str): An optional description for the server variable. CommonMark syntax MAY
                                be used for rich text representation.
        """
        super(ServerVariable, self).__init__()

        enum_values = [enum_values] if isinstance(enum_values, str) else enum_values
        self.default = default_val
        self.enum = enum_values or []
        self.description = description


class Component(ExtensionModel):
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


class Paths(ContainerModel):
    """
    Holds the relative paths to the individual endpoints and their operations. The path is appended to the URL
    from the Server Object in order to construct the full URL. The Paths MAY be empty, due to ACL constraints.
    """

    def add(self, relative_url, path_item):
        """
        Adds a path item
        Args:
          relative_url (str): path url name, eg `/echo`
          path_item (PathItem|SwaggerDict) : PathItem instance describing the path
        """

        if isinstance(path_item, PathItem):
            path_item = path_item.dict()
        super(Paths, self).add(relative_url, path_item)


class PathItem(BaseModel):
    """
    Describes the operations available on a single path. A Path Item MAY be empty, due to ACL constraints. The
    path itself is still exposed to the documentation viewer but they will not know which operations and parameters
    are available.
    """

    def __init__(self, ref=None,
                 summary=None,
                 description=None,
                 parameters=None,
                 servers=None,
                 get=None,
                 delete=None,
                 head=None,
                 options=None,
                 patch=None,
                 post=None,
                 put=None,
                 trace=None):
        super(PathItem, self).__init__()

        self.ref = ref  # type: str
        self.summary = summary  # type: str
        self.description = description  # type: str

        self.servers = servers or []  # type: list[Server]
        self.parameters = parameters or []  # type: list[Parameter]

        self.get = get  # type -> Operation
        self.delete = delete  # type -> Operation
        self.head = head  # type -> Operation
        self.options = options  # type -> Operation
        self.patch = patch  # type -> Operation
        self.post = post  # type -> Operation
        self.put = put  # type -> Operation
        self.trace = trace  # type -> Operation

    def add_operation(self, operation):
        """
        Adds an operation
        Args:
          operation (Operation): operation to add
        """
        http_method = operation.http_method.value.lower()
        setattr(self, http_method, operation)

    def add_server(self, server):
        """
        Adds an alternative server to service all operations in this path.

        Args:
            server (Server): alternative server to add
        """
        self.servers.append(server)

    def add_parameter(self, parameter):
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


class Operation(ExtensionModel):
    """ Describes a single API operation on a path. """

    def __init__(self,
                 tags=None,
                 summary=None,
                 description=None,
                 operations_id=None,
                 parameters=None):
        super(Operation, self).__init__()
        self.tags = tags  # type: list[str]
        self.summary = summary  # type: str
        self.description = description  # type: str
        self.external_docs = None
        self.operation_id = operations_id  # type: str
        self.parameters = parameters or []  # type: list[Parameter]
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
        """
        Factory for creating instances of Http Operations
        Args:
            http_method (str): http method string

        Returns:
            Operation:
        """
        http_method = HttpMethod(http_method)
        if http_method == HttpMethod.GET:
            return GET()
        elif http_method == HttpMethod.POST:
            return POST()
        elif http_method == HttpMethod.PUT:
            return PUT()
        elif http_method == HttpMethod.DELETE:
            return DELETE()
        elif http_method == HttpMethod.OPTIONS:
            return OPTIONS()
        elif http_method == HttpMethod.TRACE:
            return TRACE()
        elif http_method == HttpMethod.PATCH:
            return PATCH()
        elif http_method == HttpMethod.HEAD:
            return HEAD()


class GET(Operation):

    @property
    def http_method(self):
        return HttpMethod.GET


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


class ExternalDocumentation(ExtensionModel):
    """ Allows referencing an external resource for extended documentation. """

    def __init__(self, url, description=None):
        super(ExternalDocumentation, self).__init__()

        self.url = url
        self.description = description


class ParameterLocation(Enum):
    COOKIE = "cookie"
    HEADER = "header"
    PATH = "path"
    QUERY = "query"


class Style(Enum):
    """ Style values defined to aid serializing different simple parameters """

    FORM = "form"
    LABEL = "label"
    MATRIX = "matrix"
    SIMPLE = "simple"
    SPACE_DELIMITED = "spaceDelimited"
    PIPE_DELIMITED = "pipeDelimited"
    DEEP_OBJECT = "deepObject"


class Parameter(BaseModel):
    """
    Describes a single operation parameter.
    A unique parameter is defined by a combination of a name and location.
    """

    def __init__(self,
                 name,
                 required=False,
                 description=None,
                 deprecated=False,
                 style="form",
                 allow_empty_value=False,
                 explode=False,
                 allow_reserved=False,
                 schema=None,
                 content=None):
        super(Parameter, self).__init__()
        self.name = name  # type: str
        self._in = ParameterLocation("query")
        self.description = description  # type: str
        self.deprecated = deprecated  # type: bool
        self._required = required  # type: bool

        self.allow_empty_value = allow_empty_value  # type: bool
        self.allow_reserved = allow_reserved
        self.schema = schema
        self.content = content  # type: dict

        self.explode = explode
        self._style = style if isinstance(style, Style) else Style(style)

        self.example = None
        self.examples = None

    @property
    def q_required(self):
        return self._required

    @property
    def q_style(self):
        return self._style

    @property
    def q_in(self):
        return self._in.value


class PathParameter(Parameter):

    @property
    def q_required(self):
        return True

    @property
    def q_style(self):
        return self._style.value or Style.SIMPLE.value

    @property
    def q_in(self):
        return ParameterLocation.PATH.value


class QueryParameter(Parameter):

    @property
    def q_style(self):
        return self._style.valaue or Style.FORM.value


class HeaderParameter(Parameter):

    @property
    def q_style(self):
        return self._style.value or Style.SIMPLE.value


class CookieParameter(Parameter):

    @property
    def q_style(self):
        return self._style.value or Style.FORM.value


class RequestBody(ExtensionModel):

    def __init__(self,
                 content,
                 description=None,
                 required=None):
        super(RequestBody, self).__init__()

        self.content = content
        self.description = description  # type: str
        self.required = required  # type: bool


class MediaType(BaseModel):
    """ Each Media Type Object provides schema and examples for the media type identified by its key. """

    def __init__(self,
                 schema=None,
                 example=None,
                 examples=None,
                 encoding=None):
        super(MediaType, self).__init__()

        self.schema = schema
        self.example = example
        self.examples = examples
        self.encoding = encoding

    def add_example(self, name, example):
        self.examples[name] = example

    def add_encoding(self, name, encoding):
        self.encoding[name] = encoding


class Encoding(ExtensionModel):
    """ A single encoding definition applied to a single schema property. """

    def __init__(self,
                 content_type,
                 headers=None,
                 style=None,
                 explode=None,
                 allow_reserved=False):
        super(Encoding, self).__init__()
        self.content_type = content_type  # type: str
        self.headers = headers
        self._style = style if isinstance(style, Style) else Style(style)
        self.explode = explode  # type: bool
        self.allow_reserved = allow_reserved  # type: bool

    @property
    def style(self):
        return self._style.value

    def add_header(self, name, header):
        self.headers[name] = header


class ResponsesObject(ExtensionModel):
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
        self.default = default  # type: ResponseObject
        self.responses = {}  # type: dict[str, ResponseObject]

    def add_response(self, status_code, response):
        self.responses[status_code] = response


class ResponseObject(ExtensionModel):
    """
    Describes a single response from an API Operation, including design-time, static links to operations based on
    the response.
    """

    def __init__(self, description, headers=None, content=None, links=None):
        super(ResponseObject, self).__init__()
        self.description = description  # type: str
        self.headers = headers  # type: dict[str, Header]
        self.content = content  # type: dict[str, MediaType]
        self.links = links

    def add_header(self, name, header):
        self.headers[name] = header

    def add_content(self, media_type, content):
        if not self.content:
            self.content = SwaggerDict()
        self.content[media_type] = content

    def add_link(self, link_name, link):
        pass


class Callback(BaseModel):
    """
    A map of possible out-of band callbacks related to the parent operation. Each value in the map is a Path Item
    Object that describes a set of requests that may be initiated by the API provider and the expected responses. The
    key value used to identify the callback object is an expression, evaluated at runtime, that identifies a URL to
    use for the callback operation.
    """

    def __init__(self, expression):
        self.expression = expression  # type: PathItem


class Example(ExtensionModel):

    def __init__(self,
                 summary=None,
                 description=None,
                 value=None,
                 external_value=None):
        super(Example, self).__init__()

        self.summary = summary  # type: str
        self.description = description  # type: str
        self.value = value  # type: object
        self.external_value = external_value  # type: str


class Header(HeaderParameter):

    @property
    def required(self):
        return self._required

    @property
    def style(self):
        return self._style.value


class Link(ExtensionModel):
    """
    The Link object represents a possible design-time link for a response. The presence of a link does not guarantee
    the caller's ability to successfully invoke it, rather it provides a known relationship and traversal mechanism
    between responses and other operations. Unlike dynamic links (i.e. links provided in the response payload),
    the OAS linking mechanism does not require link information in the runtime response. For computing links,
    and providing instructions to execute them, a runtime expression is used for accessing values in an operation and
    using them as parameters while invoking the linked operation.
    """

    def __init__(self,
                 operation_ref=None,
                 operation_id=None,
                 description=None,
                 parameters=None,
                 request_body=None,
                 server=None):
        super(Link, self).__init__()
        self.operation_ref = operation_ref  # type: str
        self.operation_id = operation_id  # type: str
        self.description = description  # type: str

        self.parameters = parameters  # type: dict[str, Parameter]
        self.request_body = request_body  # type: object
        self.server = server  # type: Server


class Tag(BaseModel):

    def __init__(self,
                 name,
                 description=None,
                 external_doc=None):
        super(Tag, self).__init__()
        self.name = name  # type: str
        self.description = description  # type: str
        self._external_docs = external_doc  # type ExternalDocumentation

    def external_docs(self, url, description=None):
        self._external_docs = ExternalDocumentation(url=url, description=description)


class ReferenceObject(BaseModel):

    def __init__(self, ref):
        self.ref = ref


# TODO
class Schema(object):

    def __init__(self, schema_type, schema_format, ref=None):
        self.ref = ref  # type: str
        self.title = None
        self.multiple_of = None
        self.maximum = None
        self.exclusive_maximum = None
        self.minimum = None
        self.exclusive_minimum = None
        self.max_length = None  # type: int
        self.min_length = None  # type: int
        self.pattern = None
        self.max_items = None  # type: ignore
        self.min_items = None  # type: ignore
        self.unique_item = None
        self.max_properties = None  # type: ignore
        self.min_properties = None  # type: ignore
        self.required = None
        self.enum = None
        self.type = schema_type
        self.all_of = None
        self.one_of = None
        self.any_of = None
        self._not = None  # type: ignore
        self.items = None
        self.properties = None
        self.additional_properties = None
        self.description = None
        self.format = schema_format
        self.default = None
        self.nullable = None
        self.discriminator = None
        self.read_only = None
        self.write_only = None
        self.xml = None
        self.external_docs = None
        self.example = None
        self.deprecated = None

    def q_not(self):
        return self._not


class Discriminator(BaseModel):
    """ When request bodies or response payloads may be one of a number of different schemas, a discriminator object
    can be used to aid in serialization, deserialization, and validation. The discriminator is a specific object in a
    schema which is used to inform the consumer of the specification of an alternative schema based on the value
    associated with it. """

    def __init__(self, property_name, mapping=None):
        self.property_name = property_name
        self.mapping = mapping  # type: dict


class XML(ExtensionModel):
    """ A metadata object that allows for more fine-tuned XML model definitions. When using arrays, XML element names
    are not inferred (for singular/plural forms) and the name property SHOULD be used to add that information. See
    examples for expected behavior.
    """

    def __init__(self,
                 name,
                 namespace=None,
                 prefix=None,
                 attribute=None,
                 wrapped=None):
        super(XML, self).__init__()

        self.name = name
        self.namespace = namespace
        self.prefix = prefix
        self.attribute = attribute
        self.wrapped = wrapped


class SecuritySchemeType(Enum):

    API_KEY = "apiKey"
    HTTP = "http"
    OAUTH2 = "oauth2"
    OPEN_ID_CONNECT = "openIdConnect"


class SecurityScheme(ExtensionModel):
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


class OAuthFlows(ExtensionModel):
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


class OAuthFlow(ExtensionModel):
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


class OpenApi(BaseModel):
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
