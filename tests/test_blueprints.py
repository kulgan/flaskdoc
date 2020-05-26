import json

import pytest
import yaml


@pytest.mark.parametrize("sample", ["hulu", "polo"])
def test_route_decorator(client, sample):
    """ Tests extension registers routes as expected """
    resp = client.get("/mocks/echo/{}".format(sample))
    assert resp.status_code == 200
    assert resp.get_data(as_text=True) == sample

    post_body = dict(sample=sample, message="Almighty")
    resp = client.post("/mocks/echo", data=json.dumps(post_body))
    assert resp.status_code == 200
    assert resp.json == post_body


def test_registered_openapi(client):
    """ Tests the endpoints for downloading openapi spec was registered """

    # test availability of /openapi.json
    response = client.get("/openapi.json")
    api_docs = response.json

    info_block = api_docs["info"]
    assert info_block["contact"]["email"] == "r.ogwara@gmail.com"

    response = client.get("/openapi.yaml")
    api_docs = yaml.safe_load(response.data)
    info_block = api_docs["info"]
    assert info_block["contact"]["email"] == "r.ogwara@gmail.com"

