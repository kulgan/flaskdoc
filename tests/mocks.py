import flask

import flaskdoc
from flaskdoc import swagger

blp = flaskdoc.Blueprint("Dummy", __name__, url_prefix="/v1")

simple_get = swagger.GET(
    summary="Simplistic Get",
    tags=["test", "user", "sample"],
    description="Proof of concept",
    parameters=[
        swagger.PathParameter(
            name="id",
            description="root id",
            allow_empty_value=True,
            schema=swagger.Schema(schema_type="string", schema_format="email")
        ),
        swagger.QueryParameter(
            name="age",
            description="age of user"
        )
    ]
)

servers = [
    swagger.Server(url="https://{sample}.sample/com",
                   description="Test Suite",
                   variables=dict(
                       sample=swagger.ServerVariable(default_val="api",
                                                     enum_values=["api", "api2", "api3"])
                   ))
]


@blp.route("/echo/<string:sample>",
           ref="Simplistic",
           description="Test API Summary",
           methods=simple_get,
           servers=servers,
           )
def echo(sample):
    """
    Sample GET request
    Returns: Echos back whatever was sent

    """
    return sample


@blp.route("/echo", ref="Sponsors Cove", description="Howdy for post", methods=["POST"])
def post():
    req = flask.request.get_json(force=True)
    return flask.jsonify(req), 200
