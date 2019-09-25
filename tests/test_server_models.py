import swagger


def test_server_variable():
    sv = swagger.ServerVariable(default_val="1.0", description="version number")
    sv2 = swagger.ServerVariable("1.0", "version number")

    assert sv == sv2

    d = sv.as_dict()
    assert d["default"] == "1.0"


def test_server():
    s1 = swagger.Server(url="https://api.dund.com/{version}", description="Service Endpoint")
    s1.add_variable("version", swagger.ServerVariable("1.1", enum_values=["1.0", "1.1"]))

    d = s1.as_dict()
    assert d["variables"]
