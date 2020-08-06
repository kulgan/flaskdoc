import flask

from flaskdoc import swagger

blp = flask.Blueprint("Dummy", __name__, url_prefix="/v1")

simple_get = swagger.GET(
    summary="Simplistic Get",
    tags=["test", "user", "sample"],
    description="Proof of concept",
    parameters=[
        swagger.PathParameter(
            name="id",
            description="root id",
            allow_empty_value=True,
            schema=swagger.Schema(type="string", format="email",),
        ),
        swagger.QueryParameter(name="age", description="age of user", schema=swagger.Integer()),
    ],
    responses={"200": swagger.ResponseObject(description="Echos whatever")},
)

servers = [
    swagger.Server(
        url="https://{sample}.sample/com",
        description="Test Suite",
        variables=dict(
            sample=swagger.ServerVariable(default="api", enum=["api", "api2", "api3"],),
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
            description="Success", content=swagger.PlainText(schema=swagger.Email()),
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
    description="Posts an Echo",
    responses={"201": swagger.ResponseObject(description="OK")},
)
@blp.route("/echo", methods=["POST"])
def post():
    req = flask.request.get_json(force=True)
    return flask.jsonify(req), 200
