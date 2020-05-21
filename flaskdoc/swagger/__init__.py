from flaskdoc.swagger.models import (
    License,
    Contact,
    Info,
    Server,
    ServerVariable,
    Component,
    Paths,
    PathItem,
    Operation,
    GET,
    POST,
    PUT,
    HEAD,
    OPTIONS,
    PATCH,
    TRACE,
    HttpMethod,
    ParameterLocation,
    Style,
    Parameter,
    PathParameter,
    QueryParameter,
    HeaderParameter,
    CookieParameter,
    Tag,
    ReferenceObject,
    Schema,
    Discriminator,
    XML,
    SecuritySchemeType,
    SecurityScheme,
    OAuthFlows,
    OAuthFlow,
    OpenApi)


if __name__ == '__main__':
    pi = PathItem(ref="hello", summary="Summarize this")
    s1 = Server(description="Server Man", url="https://dd.web.com")
    pi.add_server(s1)

    get = GET(tags=["test"], summary="Yinyi de no sou", description="Kemi mi")
    get.operation_id = "getByExample"
    pr = QueryParameter(name="age", description="Just some shit")
    get.add_parameter(pr)
    pi.get = get
    ps = Paths()
    ps.add("/echo", pi)
    print(ps)

    h = HttpMethod("GET")
    print(h)
