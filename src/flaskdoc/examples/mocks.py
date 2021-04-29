import flask

from flaskdoc import swagger

blp = flask.Blueprint("mocks", __name__, url_prefix="/mocks")

simple_get = swagger.GET(
    summary="Simplistic Get",
    tags=["test", "user", "sample"],
    description="Proof of concept",
    parameters=[
        swagger.PathParameter(
            name="id",
            description="root id",
            allow_empty_value=True,
            schema=swagger.Schema(
                type="string",
                format="email",
            ),
        ),
        swagger.QueryParameter(name="age", description="age of user", schema=swagger.Integer()),
    ],
    responses={"200": swagger.ResponseObject(description="Echos whatever")},
)

info = swagger.Info(
    title="Test",
    version="1.2.2",
    contact=swagger.Contact(name="nuke", email="nuke@gmail.com", url="https://github.com/kulgan"),
    license=swagger.License(name="Apache 2.0", url="https://www.example.com/license"),
)

tags = [
    swagger.Tag(name="getEcho", description="gets echos no matter where they are hiding"),
    swagger.Tag(name="postEcho", description="posts echos to hidden locations"),
]

servers = [
    swagger.Server(
        url="https://{sample}.sample/com",
        description="Test Suite",
        variables=dict(
            sample=swagger.ServerVariable(default="api", enum=["api", "api2", "api3"]),
        ),
    ),
]


@swagger.GET(
    tags=["getEcho"],
    operation_id="getEcho",
    parameters=[swagger.PathParameter(name="sample", schema=str)],
    description="Retrieve echos wit Get",
    responses={
        "200": swagger.ResponseObject(
            description="Success",
            content=swagger.PlainText(schema=swagger.Email()),
        )
    },
)
@blp.route("/echo/<string:sample>", methods=["GET"])
def echo(sample: str):
    """
    Sample GET request
    Returns: Echos back whatever was sent

    """
    return sample


@swagger.POST(
    tags=["postEcho"],
    operation_id="postEcho",
    description="Posts an Echo",
    responses={"201": swagger.ResponseObject(description="OK")},
)
@blp.route("/echo", methods=["POST"])
def post():
    req = flask.request.get_json(force=True)
    return flask.jsonify(req), 200
