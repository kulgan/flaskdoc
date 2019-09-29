import flask

import flaskdoc
from swagger import GET, PathParameter, QueryParameter, Server, ServerVariable

blp = flaskdoc.Blueprint("Dummy", __name__, url_prefix="/v1")

simple_get = GET(
    summary="Simplistic Get",
    tags=["test", "user", "sample"],
    description="Proof of concept",
    parameters=[
        PathParameter(
            name="id",
            description="root id",
            allow_empty_value=True
        ),
        QueryParameter(
            name="age",
            description="age of user"
        )
    ]
)

servers = [
    Server(url="https://{sample}.sample/com",
           description="Test Suite",
           variables=dict(
               sample=ServerVariable(default_val="api",
                                     enum_values=["api", "api2", "api3"])
           ))
]


@blp.route("/echo",
           ref="Simplistic",
           description="Test API Summary",
           methods=simple_get,
           servers=servers,
           )
def get(sample):
    """
    Sample GET request
    Returns:

    """
    return "Echo" + sample


@blp.route("/post", ref="Sponsors Cove", description="Howdy for post", methods=["GET"])
def post():
    return flask.jsonify(dict(a="Test", message="Success")), 200
