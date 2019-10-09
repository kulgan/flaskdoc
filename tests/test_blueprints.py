import json

import pytest


@pytest.mark.parametrize("sample", ["hulu", "polo"])
def test_route_decorator(client, sample):
    """ Tests extension registers routes as expected """
    resp = client.get("/mocks/echo/{}".format(sample))
    assert resp.status_code == 200
    assert resp.data == sample

    post_body = dict(sample=sample, message="Almighty")
    resp = client.post("/mocks/echo", data=json.dumps(post_body))
    assert resp.status_code == 200
    assert resp.json == post_body
