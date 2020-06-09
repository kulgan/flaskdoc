""" Tests swagger related models and decorators """
import pytest

from flaskdoc.swagger import models


def test_dict_set_item():
    """ Test SwaggerDict instances does not allow null/empty values """

    e1 = models.SwaggerDict()
    e1["dummy"] = False
    e1["x_dummy"] = []
    e1["empty_str"] = ""

    assert e1["dummy"] is False
    assert "x_dummy" not in e1
    assert "empty_str" not in e1


def test_extension_model_usage():
    """ Tests adding and validating extensions to models """

    lc = models.License(name="Dummy License", url="http://dummy")

    with pytest.raises(ValueError) as e:
        lc.add_extension("y-breaker", "BROKEN")

    lc.add_extension("x-hulu", "HULU")

    lc_dict = lc.dict()
    assert lc_dict["x-hulu"] == "HULU"


def test_to_camel_case():
    inf = models.Info(title="Test A", version="123", terms_of_service="organized")
    inf_dict = inf.dict()

    assert inf_dict["termsOfService"] == "organized"


def test_url_property_validation():

    with pytest.raises(ValueError, match="License.url entry 'http:l//dummy' is not a valid url"):
        models.License(name="Dummy License", url="http:l//dummy")
