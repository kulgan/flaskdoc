""" Tests swagger related models and decorators """
import pytest

from flaskdoc.swagger import models


def test_dict_set_item():
    """Test SwaggerDict instances does not allow null/empty values"""

    e1 = models.SwaggerDict()
    e1["dummy"] = False
    e1["x_dummy"] = []
    e1["empty_str"] = ""

    assert e1["dummy"] is False
    assert "x_dummy" not in e1
    assert "empty_str" not in e1


def test_extension_model_usage():
    """Tests adding and validating extensions to models"""
    print("SSSSSSSSSSSSSSSSSSSSs")
    lc = models.License(name="Dummy License", url="http://dummy")

    with pytest.raises(ValueError):
        lc.add_extension("y-breaker", "BROKEN")

    lc.add_extension("x-hulu", "HULU")

    lc_dict = lc.to_dict()
    assert lc_dict["x-hulu"] == "HULU"


def test_to_camel_case():
    inf = models.Info(title="Test A", version="123", terms_of_service="organized")
    inf_dict = inf.to_dict()

    assert inf_dict["termsOfService"] == "organized"


def test_url_property_validation():

    with pytest.raises(ValueError, match="License.url entry 'http:l//dummy' is not a valid url"):
        models.License(name="Dummy License", url="http:l//dummy")


def test_nested_models():

    sv = models.ServerVariable(
        default="sample", enum=["sample", "quick"], description="dirty dozen"
    )

    server = models.Server(url="http://flaskdoc.com/{tick}", description="sample deploy site")
    server.add_variable("tick", sv)
    swagger = server.to_dict()

    variables = swagger["variables"]
    assert variables["tick"]["default"] == "sample"
    assert variables["tick"]["description"] == "dirty dozen"
