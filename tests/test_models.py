from flaskdoc import swagger


def test_license_model():
    li = swagger.License(name="Smith L.")
    d = li.to_dict()

    assert "name" in d
    assert "description" not in d

    li = swagger.License(name="Smith L.", url="https://www.example.com/license")
    li.add_extension("x-d", 1)
    d = li.to_dict()

    assert d["name"] == "Smith L."
    assert d["url"] == "https://www.example.com/license"


def test_contact_model():

    # assert
    c1 = swagger.Contact()

    d = c1.to_dict()
    assert d == {}

    c1.name = "Test Smith"
    c1.email = "smith@gmail.com"

    d = c1.to_dict()

    assert d["name"] == "Test Smith"
    assert d["email"] == "smith@gmail.com"


def test_server_variable():
    sv = swagger.ServerVariable("1.0", description="version number")
    sv2 = swagger.ServerVariable("1.0", None, "version number")

    assert sv == sv2

    d = sv.to_dict()
    assert d["default"] == "1.0"
    assert "enum" not in d


def test_server():
    s1 = swagger.Server(url="https://api.dund.com/{version}", description="Service Endpoint")
    s1.add_variable("version", swagger.ServerVariable("1.1", enum=["1.0", "1.1"]))

    d = s1.to_dict()
    assert d["variables"]


def test_path_items():
    get_op = swagger.GET(
        operation_id="testGetExample",
        description="Get Example",
        tags=["example"],
        parameters=[swagger.QueryParameter(name="p1", description="page")],
        responses=None,
    )
    post_op = swagger.POST(
        operation_id="testPostExample", description="POST Example", responses=None
    )
    path_item = swagger.PathItem(
        parameters=[swagger.PathParameter(name="v1")], get=get_op, post=post_op
    )

    swag = path_item.to_dict()
    assert swag["parameters"][0]["name"] == "v1"
    assert swag["get"]["parameters"][0]["name"] == "p1"
