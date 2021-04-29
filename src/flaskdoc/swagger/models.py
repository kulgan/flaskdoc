# Standard Library
import enum
import logging
import re
from collections import OrderedDict
from typing import Union

import attr

from flaskdoc.core import ApiDecoratorMixin, DictMixin, ExtensionMixin, ModelMixin
from flaskdoc.swagger import validators
from flaskdoc.swagger.schema import ContentMixin, schema_factory

logger = logging.getLogger(__name__)


class SwaggerDict(OrderedDict, DictMixin):
    """Used to filter out properties that are not set"""

    def __setitem__(self, key, value):
        if value not in [False, True] and not value:
            return
        super(SwaggerDict, self).__setitem__(key, value)


@attr.s
class ContainerModel(ModelMixin):

    items = attr.ib(default=SwaggerDict())

    def add(self, key, item):
        """Adds an item
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
        return self.parse(self.items)


@attr.s
class License(ExtensionMixin):
    """License information for the exposed API.

    This object MAY be extended with Specification Extensions.

    Properties:
        name: REQUIRED. The license name used for the API.
        url: A URL to the license used for the API. MUST be in the format of a URL.
    """

    name = attr.ib(type=str)
    url = attr.ib(default=None, type=str)
    extensions = attr.ib(default={})

    @url.validator
    def validate(self, _, url):
        if url:
            validators.validate_url(url, "License.url")


@attr.s
class Contact(ExtensionMixin):
    """Contact information for the exposed API.

    This object MAY be extended with Specification Extensions.

    Properties:
        name: The identifying name of the contact person/organization.
        email: The email address of the contact person/organization. MUST be in the format of an email address.
        url: The URL pointing to the contact information. MUST be in the format of a URL.
    """

    name = attr.ib(default=None, type=str)
    email = attr.ib(default=None, type=str)
    url = attr.ib(default=None, type=str)
    extensions = attr.ib(default={})

    @url.validator
    def validate(self, _, url):
        if url:
            validators.validate_url(url, "Contact.url")


@attr.s
class Info(ExtensionMixin):
    """The object provides metadata about the API.

    The metadata MAY be used by the clients if needed, and MAY be presented in editing or documentation generation
    tools for convenience. This object MAY be extended with Specification Extensions.

    Properties:
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
    extensions = attr.ib(default={})


@attr.s
class ServerVariable(ExtensionMixin):
    """An object representing a Server Variable for server URL template substitution.

    This object MAY be extended with Specification Extensions.

    Properties:
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
    extensions = attr.ib(default={})


@attr.s
class Server(ExtensionMixin):
    """An object representing a Server.

    This object MAY be extended with Specification Extensions.

    Properties:
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
    variables = attr.ib(default=None, type=dict)
    extensions = attr.ib(default={})

    def add_variable(self, name: str, variable: ServerVariable):
        """Adds a server variable
        Args:
            name: variable name
            variable: Server variable instance
        """
        if not self.variables:
            self.variables = {}
        self.variables[name] = variable


class Style(enum.Enum):
    """Style values defined to aid serializing different simple parameters"""

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

    _ref_object = attr.ib(default="schemas", init=False)

    def __attrs_post_init__(self):
        if "#/components" not in self.ref:
            self.ref = "#/components/{}/{}".format(self._ref_object, self.ref)

    def to_dict(self):
        return {"$ref": self.ref}


@attr.s
class ExampleReference(ReferenceObject):
    _ref_object = attr.ib(default="examples", init=False)


@attr.s
class LinkReference(ReferenceObject):
    _ref_object = attr.ib(default="links", init=False)


@attr.s
class ExternalDocumentation(ExtensionMixin):
    """Allows referencing an external resource for extended documentation."""

    url = attr.ib(type=str)
    description = attr.ib(default=None, type=str)
    extensions = attr.ib(default={})


@attr.s
class RequestBody(ContentMixin, ExtensionMixin):

    description = attr.ib(default=None, type=str)
    required = attr.ib(default=None)
    extensions = attr.ib(default={})


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
class Parameter(ExtensionMixin, ApiDecoratorMixin):
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
    content = attr.ib(default=None)
    explode = attr.ib(default=None)
    _style = attr.ib(default=None, type=Style, init=False)
    example = attr.ib(default=None)
    examples = attr.ib(default=None, type=dict)
    extensions = attr.ib(default={})

    @property
    def q_in(self):
        return self._in.value

    @property
    def q_style(self):
        return self._style.value

    def __attrs_post_init__(self):
        if self.schema:
            self.schema = schema_factory.get_schema(self.schema)

    def merge(self, parameter):
        if self.required is None:
            self.required = parameter.required
        if self.schema is None:
            self.schema = parameter.schema
        if self.content is None:
            self.content = parameter.content


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
    _style = attr.ib(default=Style.SIMPLE, init=False)


@attr.s
class CookieParameter(Parameter):

    _in = attr.ib(default=ParameterLocation.COOKIE, init=False)
    _style = attr.ib(default=Style.FORM, init=False)


@attr.s
class Header(HeaderParameter):

    name = attr.ib(default=None, init=False)
    _in = attr.ib(default=None, init=False)


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
    extensions = attr.ib(default={})


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
    extensions = attr.ib(default={})

    def add_header(self, name: str, header: Union[ReferenceObject, HeaderParameter]):
        if self.headers is None:
            self.headers = SwaggerDict()
        self.headers[name] = header

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
    responses = attr.ib(default=None, type=dict)
    extensions = attr.ib(default={})

    def add_response(self, status_code: str, response: ResponseObject):
        self.responses[status_code] = response


@attr.s
class Tag(ExtensionMixin, ApiDecoratorMixin):

    name = attr.ib(type=str)
    description = attr.ib(default=None, type=str)
    external_docs = attr.ib(default=None, type=ExternalDocumentation)
    extensions = attr.ib(default={})

    def external_doc(self, url, description=None):
        self.external_docs = ExternalDocumentation(url=url, description=description)


@attr.s
class Operation(ExtensionMixin, ApiDecoratorMixin):
    """Describes a single API operation on a path."""

    responses = attr.ib(type=dict)
    tags = attr.ib(default=None, type=list)
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
    extensions = attr.ib(default={})

    @property
    def http_method(self):
        return None

    def add_parameter(self, parameter: Union[Parameter, ReferenceObject]):
        if self.parameters is None:
            self.parameters = []
        self.parameters.append(parameter)

    @staticmethod
    def from_op(http_method: str, responses: SwaggerDict):
        """Factory for creating instances of Http Operations"""

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
class PathItem(ExtensionMixin):
    """
    Describes the operations available on a single path. A Path Item MAY be empty, due to ACL constraints. The
    path itself is still exposed to the documentation viewer but they will not know which operations and parameters
    are available.
    """

    ref = attr.ib(default=None, type=str)
    summary = attr.ib(default=None, type=str)
    description = attr.ib(default=None, type=str)

    servers = attr.ib(default=None, type=list)
    parameters = attr.ib(default=None, type=list)

    get = attr.ib(default=None, type=Operation)
    delete = attr.ib(default=None, type=Operation)
    head = attr.ib(default=None, type=Operation)
    options = attr.ib(default=None, type=Operation)
    patch = attr.ib(default=None, type=Operation)
    post = attr.ib(default=None, type=Operation)
    put = attr.ib(default=None, type=Operation)
    trace = attr.ib(default=None, type=Operation)
    extensions = attr.ib(default={})

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
        for param in self.parameters:
            if param.name == parameter.name:
                # previously added
                param.merge(parameter)
                return
        self.parameters.append(parameter)

    def merge_path_item(self, path_item):
        """
        Merges another path item into this on
        Args:
            path_item (PathItem): PathItem instance to merge
        """
        for server in path_item.servers or []:
            self.add_server(server)

        for param in path_item.parameters or []:
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


@attr.s
class GET(Operation):
    @property
    def http_method(self):
        return HttpMethod.GET


@attr.s
class POST(Operation):
    @property
    def http_method(self):
        return HttpMethod.POST


@attr.s
class PUT(Operation):
    @property
    def http_method(self):
        return HttpMethod.PUT


@attr.s
class HEAD(Operation):
    @property
    def http_method(self):
        return HttpMethod.HEAD


@attr.s
class OPTIONS(Operation):
    @property
    def http_method(self):
        return HttpMethod.OPTIONS


@attr.s
class PATCH(Operation):
    @property
    def http_method(self):
        return HttpMethod.PATCH


@attr.s
class TRACE(Operation):
    @property
    def http_method(self):
        return HttpMethod.TRACE


@attr.s
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


@attr.s
class SecurityScheme(ExtensionMixin):
    """Defines a security scheme that can be used by the operations.

    Supported schemes are HTTP authentication, an API key (either as a header or as a query parameter), OAuth2's
    common flows (implicit, password, application and access code) as defined in RFC6749, and OpenID Connect Discovery.
    """

    _type = attr.ib(type=str, init=False)

    @property
    def q_type(self):
        if self._type:
            return self._type.value


@attr.s
class ApiKeySecurityScheme(SecurityScheme):
    """OpenAPI security scheme definition with type apiKey

    Example:
        Sample security requirements
        .. code-block:: json

            {
                "api_key": []
            }
    """

    name = attr.ib(type=str)
    _type = attr.ib(default=SecuritySchemeType.API_KEY, init=False)
    _in = attr.ib(default=ParameterLocation.HEADER, init=False)
    description = attr.ib(default=None, type=str)
    extensions = attr.ib(default={})

    @property
    def q_in(self):
        return self._in.value


@attr.s
class HttpSecurityScheme(SecurityScheme):
    """OpenAPI security scheme definition with type http"""

    scheme = attr.ib(type="string")
    bearer_format = attr.ib(default="bearer")
    description = attr.ib(default=None, type=str)
    _type = attr.ib(default=SecuritySchemeType.HTTP, init=False)
    extensions = attr.ib(default={})


@attr.s
class OpenIDConnectScheme(SecurityScheme):
    """OpenAPI security scheme definition with type openidConnect"""

    open_id_connect_url = attr.ib(type=str)
    _type = attr.ib(default=SecuritySchemeType.OPEN_ID_CONNECT, init=False)
    extensions = attr.ib(default={})

    @open_id_connect_url.validator
    def validate(self, _, url):
        if url:
            validators.validate_url(url, "OpenIDConnectScheme.open_id_connect_url")


@attr.s
class OAuth2SecurityScheme(SecurityScheme):
    """OpenAPI security scheme definition with type oauth2"""

    flows = attr.ib()
    _type = attr.ib(default=SecuritySchemeType.OAUTH2, init=False)
    extensions = attr.ib(default={})


class ImplicitOAuthFlow(ExtensionMixin):
    """Implicit OAuth2 Flow"""

    def __init__(self, authorization_url, scopes, token_url=None, refresh_url=None):
        self.implicit = OAuthFlow(
            authorization_url=authorization_url,
            token_url=token_url,
            refresh_url=refresh_url,
            scopes=scopes,
        )


class AuthorizationCodeOAuthFlow(ExtensionMixin):
    """Authorization Code OAuth2 Flow"""

    def __init__(self, authorization_url, token_url, scopes, refresh_url=None, extensions=None):
        self.authorization_code = OAuthFlow(
            authorization_url=authorization_url,
            token_url=token_url,
            refresh_url=refresh_url,
            scopes=scopes,
            extensions=extensions,
        )


class PasswordOAuthFlow(ExtensionMixin):
    """Password based OAuth2 Flow"""

    def __init__(
        self, token_url, scopes, authorization_url=None, refresh_url=None, extensions=None
    ):
        self.password = OAuthFlow(
            authorization_url=authorization_url,
            token_url=token_url,
            refresh_url=refresh_url,
            scopes=scopes,
            extensions=extensions,
        )


class ClientCredentialsOAuthFlow(ExtensionMixin):
    """Client Credentials OAuth FLow"""

    def __init__(
        self, token_url, scopes, authorization_url=None, refresh_url=None, extensions=None
    ):
        self.clientCredentials = OAuthFlow(
            authorization_url=authorization_url,
            token_url=token_url,
            refresh_url=refresh_url,
            scopes=scopes,
            extensions=extensions,
        )


@attr.s
class OAuthFlow(ExtensionMixin):
    """Configuration details for a supported OAuth Flow"""

    authorization_url = attr.ib(type=str)
    token_url = attr.ib(type=str)
    refresh_url = attr.ib(type=str)
    scopes = attr.ib(type={})
    extensions = attr.ib(default={})


class ComponentType(enum.Enum):

    EXAMPLE = "examples"
    CALLBACKS = "callbacks"
    HEADER = "headers"
    LINK = "links"
    PARAMETER = "parameters"
    REQUEST_BODY = "request+bodies"
    RESPONSE = "responses"
    SCHEMA = "schemas"
    SECURITY_SCHEME = "security_schemes"


@attr.s
class Components(ExtensionMixin):
    """Holds a set of reusable objects for different aspects of the OAS.

    All objects defined within the components object will have no effect on the API unless they are explicitly
    referenced from properties outside the components object.
    """

    schemas = attr.ib(default=None, type=dict)
    responses = attr.ib(default=None, type=dict)
    parameters = attr.ib(default=None, type=dict)
    examples = attr.ib(default=None, type=dict)
    request_bodies = attr.ib(default=None, type=dict)
    headers = attr.ib(default=None, type=dict)
    security_schemes = attr.ib(default=None, type=dict)
    links = attr.ib(default=None, type=dict)
    callbacks = attr.ib(default=None, type=dict)
    extensions = attr.ib(default={})

    PATTERN = re.compile("^[a-zA-Z0-9.-_]+$")

    def add_component(self, component_type, components):
        """Adds components

        Args:
            component_type (ComponentType): type of component
            components (dict[str, Any]): key value mapping of components
        Raises:
            ValueError: If key is not a valid value for regex ``^[a-zA-Z0-9.-_]+$``
        """
        if not components:
            return

        attrib_name = component_type.value
        values = getattr(self, attrib_name)
        if values is None:
            values = {}
            setattr(self, attrib_name, values)
        for key, component in components.items():
            Components.PATTERN.match(key)
            values[key] = component


class OpenApi(ModelMixin):
    """This is the root document object of the OpenAPI document.

    OpenApi specs tree, contains the overall specs for the API
    Properties:
        openapi (str): Open API version used by API
        info (flaskdoc.swagger.info.Info): open api info object
        paths (Paths): Paths definitions
    """

    def __init__(
        self,
        info,
        paths,
        version="3.0.3",
        tags=None,
        servers=None,
        external_docs=None,
        components=None,
    ):
        self.info = info
        self.paths = paths
        self.openapi = version
        self.tags = tags or []
        self.servers = servers or []
        self.components = components or Components()
        self.external_docs = external_docs

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
