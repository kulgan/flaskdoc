import swagger
from swagger import License, Contact


def test_license_model():
    li = License(name="Smith L.")
    d = li.as_dict()

    assert "name" in d
    assert "description" not in d

    li = License(name="Smith L.", url="https://www.example.com/license")
    d = li.as_dict()

    assert d["name"] == "Smith L."
    assert d["url"] == "https://www.example.com/license"


def test_contact_model():

    # assert
    c1 = Contact()

    d = c1.as_dict()
    assert d == {}

    c1.name = "Test Smith"
    c1.email = "smith@gmail.com"

    d = c1.as_dict()

    assert d["name"] == "Test Smith"
    assert d["email"] == "smith@gmail.com"


def test_server_variable():
    sv = swagger.ServerVariable(default_val="1.0", description="version number")
    sv2 = swagger.ServerVariable("1.0", None, "version number")

    assert sv == sv2

    d = sv.as_dict()
    assert d["default"] == "1.0"
    assert "enum" not in d


def test_server():
    s1 = swagger.Server(url="https://api.dund.com/{version}", description="Service Endpoint")
    s1.add_variable("version", swagger.ServerVariable("1.1", enum_values=["1.0", "1.1"]))

    d = s1.as_dict()
    assert d["variables"]