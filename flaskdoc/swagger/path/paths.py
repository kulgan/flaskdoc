import swagger.models
from swagger import Server, Paths, PathItem, QueryParameter

if __name__ == '__main__':
    pi = PathItem(ref="hello", summary="Summarixe this")
    s1 = Server(description="Server Man", url="https://dd.web.com")
    pi.add_server(s1)

    get = swagger.models.GET(tags=["test"], summary="Yinyi de no sou", description="Kemi mi")
    get.operation_id = "getByExample"
    pr = QueryParameter(name="age", description="Just some shit")
    get.add_parameter(pr)
    pi.get = get
    ps = Paths()
    ps.add("/echo", pi)
    # print(ps)

    h = swagger.models.HttpMethod("GETs")
    print(h)