import flask

from flaskdoc import swagger

api = flask.Blueprint("api-examples", __name__, url_prefix="/api-with-examples")

info = swagger.Info(title="Simple API Overview", version="2.0.0")

examples = {
    "foo": swagger.Example(
        value={
            "versions": [
                {
                    "status": "CURRENT",
                    "updated": "2011-01-21T11:33:21Z",
                    "id": "v2.0",
                    "links": [{"href": "http://127.0.0.1:8774/v2/", "rel": "self"}],
                },
                {
                    "status": "EXPERIMENTAL",
                    "updated": "2013-07-23T11:33:21Z",
                    "id": "v3.0",
                    "links": [{"href": "http://127.0.0.1:8774/v3/", "rel": "self"}],
                },
            ]
        }
    ),
    "v2-foo": swagger.Example(
        value={
            "version": {
                "status": "CURRENT",
                "updated": "2011-01-21T11:33:21Z",
                "media-types": [
                    {
                        "base": "application/xml",
                        "type": "application/vnd.openstack.compute+xml;version=2",
                    },
                    {
                        "base": "application/json",
                        "type": "application/vnd.openstack.compute+json;version=2",
                    },
                ],
                "id": "v2.0",
                "links": [
                    {"href": "http://23.253.228.211:8774/v2/", "rel": "self"},
                    {
                        "href": "http://docs.openstack.org/api/openstack-compute/2/os-compute-devguide-2.pdf",
                        "type": "application/pdf",
                        "rel": "describedby",
                    },
                    {
                        "href": "http://docs.openstack.org/api/openstack-compute/2/wadl/os-compute-2.wadl",
                        "type": "application/vnd.sun.wadl+xml",
                        "rel": "describedby",
                    },
                ],
            }
        }
    ),
}


@swagger.GET(
    tags=["listVersionsv2"],
    summary="List API versions",
    responses={
        "200": swagger.ResponseObject(
            description="200 response",
            content=swagger.JsonType(examples={"foo": swagger.ExampleReference("foo")}),
        ),
        "300": swagger.ResponseObject(
            description="300 response",
            content=swagger.JsonType(examples={"foo": swagger.ExampleReference("foo")}),
        ),
    },
)
@api.route("/", methods=["GET"])
def root():
    return flask.jsonify(examples["foo"])


@swagger.GET(
    tags=["getVersionDetailsv2"],
    summary="Show API versions details",
    responses={
        "200": swagger.ResponseObject(
            description="200 response",
            content=swagger.JsonType(examples={"foo": swagger.ExampleReference("v2-foo")}),
        ),
        "300": swagger.ResponseObject(
            description="300 response",
            content=swagger.JsonType(examples={"foo": swagger.ExampleReference("v2-foo")}),
        ),
    },
)
@api.route("/v2", methods=["GET"])
def details():
    return flask.jsonify(examples["v2-foo"])
