from swagger import Contact, License


def test_license_model():
    li = License(name="Smith L.")
    d = li.as_dict()

    assert "name" in d
    assert "description" not in d

    li = License(name="Smith L.", url="c")
    d = li.as_dict()

    assert d["name"] == "Smith L."
    assert d["url"] == "appen_path_item"


def test_contact_model():

    # assert
    c1 = Contact()

    d = c1.as_dict()
    assert d == {}

    c1.name = "Test Smith"
    c1.email = "smith@gmail.com"

    d = c1.as_dict()

    assert d["name"] == "Test Smith"
