# Standard Library
import enum
import logging
from collections import OrderedDict
from typing import Type, Union

import attr

from flaskdoc.core import ApiDecoratorMixin, DictMixin, ModelMixin
from flaskdoc.schema import ContentMixin, Schema, schema_factory
from flaskdoc.swagger import validators

logger = logging.getLogger(__name__)


class SwaggerDict(OrderedDict, DictMixin):
    """ Used to filter out properties that are not set """

    def __setitem__(self, key, value):
        if value not in [False, True] and not value:
            return
        super(SwaggerDict, self).__setitem__(key, value)


@attr.s
class ExtensionMixin(ModelMixin):

    extensions = attr.ib(default=None, init=False)

    def add_extension(self, name, value):
        """ Allows extensions to the Swagger Schema.

        The field name MUST begin with x-, for example, x-internal-id. The value can be null, a primitive,
        an array or an object.
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
    def validate_extension_name(value):
        """
        Validates a custom extension name
        Args:
            value (str): custom extension name
        Raises:
            ValueError: if key name is invalid
        """
        if value and not value.startswith("x-"):
            raise ValueError("Custom extension must start with x-")

    def to_dict(self):
        di = super(ExtensionMixin, self).to_dict()
        if self.extensions:
            di.update(self.extensions)
        return di


@attr.s
class ContainerModel(ModelMixin):

    items = attr.ib(default=SwaggerDict())

    def add(self, key, item):
        """ Adds an item
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

    def to_dict(self):
        return self._parse_dict(self.items)


@attr.s
class License(ExtensionMixin):
    """ License information for the exposed API.

    This object MAY be extended with Specification Extensions.

    Attributes:
        name: REQUIRED. The license name used for the API.
        url: A URL to the license used for the API. MUST be in the format of a URL.
    """

    name = attr.ib(type=str)
    url = attr.ib(default=None, type=str)

    @url.validator
    def validate(self, _, url):
        if url:
            validators.validate_url(url, "License.url")


@attr.s
class Contact(ExtensionMixin):
    """ Contact information for the exposed API.

    This object MAY be extended with Specification Extensions.

    Attributes:
          name: The identifying name of the contact person/organization.
          email: The email address of the contact person/organization. MUST be in the format of an email address.
          url: The URL pointing to the contact information. MUST be in the format of a URL.
    """

    name = attr.ib(default=None, type=str)
    email = attr.ib(default=None, type=str)
    url = attr.ib(default=None, type=str)

    @url.validator
    def validate(self, _, url):
        if url:
            validators.validate_url(url, "Contact.url")


@attr.s
class Info(ExtensionMixin):
    """ The object provides metadata about the API.

    The metadata MAY be used by the clients if needed, and MAY be presented in editing or documentation generation
    tools for convenience. This object MAY be extended with Specification Extensions.

    Attributes:
        title: REQUIRED. The title of the API.
        version: REQUIRED. The version of the OpenAPI document (which is distinct from the OpenAPI Specification
                version or the API implementation version).
        description: A short description of the API. CommonMark syntax MAY be used for rich text representation.
        terms_of_service: A URL to the Terms of Service for the API. MUST be in the format of a URL.
        contact: The contact information for the exposed API.
        license: The license information for the exposed API.
    """

    title = attr.ib(type=str)
    version = attr.ib(type=str)
    description = attr.ib(default=None, type=str)
    terms_of_service = attr.ib(default=None, type=str)
    contact = attr.ib(default=None, type=Contact)
    license = attr.ib(default=None, type=License)


@attr.s
class ServerVariable(ExtensionMixin):
    """ An object representing a Server Variable for server URL template substitution.

    This object MAY be extended with Specification Extensions.

    Attributes:
        default: REQUIRED. The default value to use for substitution, which SHALL be sent if an alternate
                value is not supplied. Note this behavior is different than the Schema Object's treatment of default
                values, because in those cases parameter values are optional.
        enum: An enumeration of string values to be used if the substitution options are from a limited set
        description: An optional description for the server variable. CommonMark syntax MAY be used for rich text
                    representation.

    """

    default = attr.ib(type=str)
    enum = attr.ib(default=None, type=list)
    description = attr.ib(default=None, type=str)


@attr.s
class Server(ExtensionMixin):
    """ An object representing a Server.

    This object MAY be extended with Specification Extensions.

    Attributes:
        url: REQUIRED. A URL to the target host. This URL supports Server Variables and MAY be relative, to indicate
            that the host location is relative to the location where the OpenAPI document is being served. Variable
            substitutions will be made when a variable is named in {brackets}.
        description: An optional string describing the host designated by the URL. CommonMark syntax MAY be used for
                     rich text representation.
        variables: A map between a variable name and its value. The value is used for substitution in the server's
                   URL template.
    """

    url = attr.ib(type=str)
    description = attr.ib(default=None, type=str)
    variables = attr.ib(default={}, type=str)

    def add_variable(self, name: str, variable: ServerVariable):
        """ Adds a server variable
        Args:
            name: variable name
            variable: Server variable instance
        """
        self.variables[name] = variable


class Style(enum.Enum):
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


@attr.s
class ReferenceObject(ModelMixin):

    ref = attr.ib(type=str)


@attr.s
class Discriminator(ModelMixin):
    """ When request bodies or response payloads may be one of a number of different schemas, a discriminator object
    can be used to aid in serialization, deserialization, and validation. The discriminator is a specific object in a
    schema which is used to inform the consumer of the specification of an alternative schema based on the value
    associated with it. """

    property_name = attr.ib(type=str)
    mapping = attr.ib(default=dict)


@attr.s
class XML(ExtensionMixin):
    """ A metadata object that allows for more fine-tuned XML model definitions. When using arrays, XML element names
    are not inferred (for singular/plural forms) and the name property SHOULD be used to add that information. See
    examples for expected behavior.
    """

    name = attr.ib(default=None, type=str)
    namespace = attr.ib(default=None, type=str)
    prefix = attr.ib(default=None, type=str)
    attribute = attr.ib(default=False)
    wrapped = attr.ib(default=False)


@attr.s
class ExternalDocumentation(ExtensionMixin):
    """ Allows referencing an external resource for extended documentation. """

    url = attr.ib(type=str)
    description = attr.ib(default=None, type=str)


@attr.s
class Encoding(ExtensionMixin):
    """ A single encoding definition applied to a single schema property. """

    content_type = attr.ib(type=str)
    headers = attr.ib(default=SwaggerDict())
    style = attr.ib(default=None, type=Style)
    explode = attr.ib(default=True)
    allow_reserved = attr.ib(default=False)

    def add_header(self, name, header):
        if not self.headers:
            self.headers = SwaggerDict()
        self.headers[name] = header


@attr.s
class Example(ExtensionMixin):

    summary = attr.ib(default=None, type=str)
    description = attr.ib(default=None, type=str)
    value = attr.ib(default=None)
    external_value = attr.ib(default=None, type=str)


@attr.s
class MediaType(ModelMixin):
    """ Each Media Type Object provides schema and examples for the media type identified by its key. """

    schema = attr.ib(default=None, type=Schema)
    example = attr.ib(default=None)
    examples = attr.ib(default=None, type=dict)
    encoding = attr.ib(default=None, type=dict)

    def add_example(self, name: str, example: Union[Example, ReferenceObject]):
        if self.examples is None:
            self.examples = SwaggerDict()
        self.examples[name] = example

    def add_encoding(self, name: str, encoding: Encoding):
        if self.encoding is None:
            self.encoding = SwaggerDict()
        self.encoding[name] = encoding


@attr.s
class RequestBody(ContentMixin, ExtensionMixin):

    description = attr.ib(default=None, type=str)
    required = attr.ib(default=False)


@attr.s
class Component(ExtensionMixin):
    """ Holds a set of reusable objects for different aspects of the OAS.

    All objects defined within the components object will have no effect on the API unless they are explicitly
    referenced from properties outside the components object.

    This object MAY be extended with Specification Extensions. All the fixed fields declared above are objects that
    MUST use keys that match the regular expression: ^[a-zA-Z0-9\\.\\-_]+$.

    Attributes:
        schemas: An object to hold reusable Schema Objects.
    """

    schemas = attr.ib(default={})
    responses = attr.ib(default={})
    parameters = attr.ib(default={})
    examples = attr.ib(default={})
    request_bodies = attr.ib(default={})
    headers = attr.ib(default={})
    security_schemes = attr.ib(default={})
    links = attr.ib(default={})
    callbacks = attr.ib(default={})

    def add_schema(self, schema_name: str, schema: Schema):
        self.schemas[schema_name] = schema

    def add_response(self, response_name: str, response):
        self.responses[response_name] = response


@attr.s
class RelativePath(object):

    url = attr.ib(type=str)
    len = attr.ib(default=0, type=int)
    params = attr.ib(default={})

    def __attrs_post_init__(self):
        self.parse(self.url)

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


class ParameterLocation(enum.Enum):
    COOKIE = "cookie"
    HEADER = "header"
    PATH = "path"
    QUERY = "query"

    def __repr__(self):
        return self.value


@attr.s
class Parameter(ModelMixin, ApiDecoratorMixin):
    """
    Describes a single operation parameter.
    A unique parameter is defined by a combination of a name and location.
    """

    name = attr.ib(type=str)
    _in = attr.ib(default=None, type=ParameterLocation, init=False)
    required = attr.ib(default=None)
    description = attr.ib(default=None, type=str)
    deprecated = attr.ib(default=None)
    allow_empty_value = attr.ib(default=None)
    allow_reserved = attr.ib(default=None)
    schema = attr.ib(default=None)
    content = attr.ib(default={})
    explode = attr.ib(default=None)
    _style = attr.ib(default=None, type=Style, init=False)
    example = attr.ib(default=None)
    examples = attr.ib(default=SwaggerDict())

    @property
    def q_in(self):
        return self._in.value

    @property
    def q_style(self):
        return self._style.value

    def __attrs_post_init__(self):
        if self.schema:
            self.schema = schema_factory.get_schema(self.schema)


@attr.s
class PathParameter(Parameter):

    _in = attr.ib(default=ParameterLocation.PATH, init=False)
    required = attr.ib(default=True, init=False)
    _style = attr.ib(default=Style.SIMPLE, init=False)


@attr.s
class QueryParameter(Parameter):

    _in = attr.ib(default=ParameterLocation.QUERY, init=False)
    _style = attr.ib(default=Style.FORM, init=False)


@attr.s
class HeaderParameter(Parameter):

    _in = attr.ib(default=ParameterLocation.HEADER, init=False)
    _styl = attr.ib(default=Style.SIMPLE, init=False)


@attr.s
class CookieParameter(Parameter):

    _in = attr.ib(default=ParameterLocation.COOKIE, init=False)
    _style = attr.ib(default=Style.FORM, init=False)


@attr.s
class Link(ExtensionMixin):
    """
    The Link object represents a possible design-time link for a response. The presence of a link does not guarantee
    the caller's ability to successfully invoke it, rather it provides a known relationship and traversal mechanism
    between responses and other operations. Unlike dynamic links (i.e. links provided in the response payload),
    the OAS linking mechanism does not require link information in the runtime response. For computing links,
    and providing instructions to execute them, a runtime expression is used for accessing values in an operation and
    using them as parameters while invoking the linked operation.
    """

    operation_ref = attr.ib(default=None, type=str)
    operation_id = attr.ib(default=None, type=str)
    description = attr.ib(default=None, type=str)
    parameters = attr.ib(default=None, type=SwaggerDict)
    request_body = attr.ib(default=None)
    server = attr.ib(default=None, type=Server)


@attr.s
class ResponseObject(ContentMixin, ExtensionMixin):
    """
    Describes a single response from an API Operation, including design-time, static links to operations based on
    the response.
    """

    description = attr.ib(type=str)
    content = attr.ib(default=None, type=SwaggerDict)
    headers = attr.ib(default=None, type=SwaggerDict)
    links = attr.ib(default=None, type=SwaggerDict)

    def add_header(self, name: str, header: Union[ReferenceObject, HeaderParameter]):
        if self.headers is None:
            self.headers = SwaggerDict()
        self.headers[name] = header

    def add_content(self, media_type: str, content: Union[MediaType, Type]):
        if not self.content:
            self.content = SwaggerDict()
        self.content[media_type] = content

    def add_link(self, link_name: str, link: Union[Link, ReferenceObject]):
        if self.links is None:
            self.links = SwaggerDict()
        self.links[link_name] = link


@attr.s
class ResponsesObject(ExtensionMixin):
    """
    A container for the expected responses of an operation. The container maps a HTTP response code to the
    expected response. The documentation is not necessarily expected to cover all possible HTTP response codes
    because they may not be known in advance. However, documentation is expected to cover a successful operation
    response and any known errors. The default MAY be used as a default response object for all HTTP codes that are
    not covered individually by the specification. The Responses Object MUST contain at least one response code,
    and it SHOULD be the response for a successful operation call.
    """

    default = attr.ib(default=None, type=ResponseObject)
    responses = attr.ib(default=SwaggerDict())

    def add_response(self, status_code: str, response: ResponseObject):
        self.responses[status_code] = response


@attr.s
class Tag(ModelMixin, ApiDecoratorMixin):

    name = attr.ib(type=str)
    description = attr.ib(default=None, type=str)
    external_docs = attr.ib(default=None, type=ExternalDocumentation)

    def external_doc(self, url, description=None):
        self.external_docs = ExternalDocumentation(url=url, description=description)


@attr.s
class Operation(ExtensionMixin, ApiDecoratorMixin):
    """ Describes a single API operation on a path. """

    responses = attr.ib(type=dict)
    tags = attr.ib(default=[], type=list)
    summary = attr.ib(default=None, type=str)
    description = attr.ib(default=None, type=str)
    external_docs = attr.ib(default=None, type=ExternalDocumentation)
    operation_id = attr.ib(default=None, type=str)
    parameters = attr.ib(default=None, type=list)
    request_body = attr.ib(default=None)
    callbacks = attr.ib(default=None, type=SwaggerDict)
    deprecated = attr.ib(default=None)
    security = attr.ib(default=None, type=list)
    servers = attr.ib(default=None, type=list)

    @property
    def http_method(self):
        return None

    def add_parameter(self, parameter: Union[Parameter, ReferenceObject]):
        if self.parameters is None:
            self.parameters = []
        self.parameters.append(parameter)

    @staticmethod
    def from_op(http_method: str, responses: SwaggerDict):
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


@attr.s
class PathItem(ModelMixin):
    """
    Describes the operations available on a single path. A Path Item MAY be empty, due to ACL constraints. The
    path itself is still exposed to the documentation viewer but they will not know which operations and parameters
    are available.
    """

    ref = attr.ib(default=None, type=str)
    summary = attr.ib(default=None, type=str)
    description = attr.ib(default=None, type=str)

    servers = attr.ib(default=[], type=list)
    parameters = attr.ib(default=[], type=list)

    get = attr.ib(default=None, type=Operation)
    delete = attr.ib(default=None, type=Operation)
    head = attr.ib(default=None, type=Operation)
    options = attr.ib(default=None, type=Operation)
    patch = attr.ib(default=None, type=Operation)
    post = attr.ib(default=None, type=Operation)
    put = attr.ib(default=None, type=Operation)
    trace = attr.ib(default=None, type=Operation)

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

    def add(self, relative_url, path_item):
        """
        Adds a path item
        Args:
          relative_url (str): path url name, eg `/echo`
          path_item (PathItem|SwaggerDict) : PathItem instance describing the path
        """

        if relative_url in self.items:
            pi = self.get(relative_url)  # type: PathItem
            pi.merge_path_item(path_item)
            return
        super(Paths, self).add(relative_url, path_item)


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


@attr.s
class Callback(ModelMixin):
    """
    A map of possible out-of band callbacks related to the parent operation. Each value in the map is a Path Item
    Object that describes a set of requests that may be initiated by the API provider and the expected responses. The
    key value used to identify the callback object is an expression, evaluated at runtime, that identifies a URL to
    use for the callback operation.
    """

    expression = attr.ib(type=PathItem)


class SecuritySchemeType(enum.Enum):

    API_KEY = "apiKey"
    HTTP = "http"
    OAUTH2 = "oauth2"
    OPEN_ID_CONNECT = "openIdConnect"


class SecurityScheme(ExtensionMixin):
    """ Defines a security scheme that can be used by the operations. Supported schemes are HTTP authentication,
    an API key (either as a header or as a query parameter), OAuth2's common flows (implicit, password, application
    and access code) as defined in RFC6749, and OpenID Connect Discovery. """

    def __init__(
        self,
        scheme_type,
        name,
        description=None,
        scheme=None,
        bearer_format=None,
        flows=None,
        open_id_connect_url=None,
    ):
        super(SecurityScheme, self).__init__()

        self.type = (
            SecuritySchemeType(scheme_type) if isinstance(scheme_type, str) else scheme_type
        )
        self.name = name  # type: str
        self.description = description  # type: str
        self.scheme = scheme  # type: str
        self.bearer_format = bearer_format  # type: str
        self.flows = flows
        self.open_id_connect_url = open_id_connect_url


class OAuthFlows(ExtensionMixin):
    """ Allows configuration of the supported OAuth Flows. """

    def __init__(
        self, implicit=None, password=None, client_credentials=None, authorization_code=None,
    ):
        super(OAuthFlows, self).__init__()

        self.implicit = implicit  # type: OAuthFlow
        self.password = password  # type: OAuthFlow
        self.client_credentials = client_credentials  # type: OAuthFlow
        self.authorization_code = authorization_code  # type: OAuthFlow


class OAuthFlow(ExtensionMixin):
    """ Configuration details for a supported OAuth Flow """

    def __init__(self, authorization_url=None, token_url=None, refresh_url=None, scopes=None):
        super(OAuthFlow, self).__init__()

        self.authorization_url = authorization_url  # type: str
        self.token_url = token_url  # type: str
        self.refresh_url = refresh_url  # type: str
        self.scopes = scopes  # type: dict


@attr.s
class OpenApi(ModelMixin):
    """ This is the root document object of the OpenAPI document.

        OpenApi specs tree, contains the overall specs for the API
        Arguments:
            openapi (str): Open API version used by API
            info (flaskdoc.swagger.info.Info): open api info object
            paths (Paths): Paths definitions
    """

    info = attr.ib(type=Info)
    paths = attr.ib(type=Paths)
    openapi = attr.ib(default="3.0.2")
    tags = attr.ib(default=[], type=list)
    servers = attr.ib(default=None, type=set)
    security = attr.ib(default=[])
    external_docs = attr.ib(default=None)
    components = attr.ib(default={}, type=dict, init=False)

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
