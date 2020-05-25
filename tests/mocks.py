import flask

import flaskdoc
from flaskdoc import swagger

blp = flask.Blueprint("Dummy", __name__, url_prefix="/v1")

simple_get = swagger.GET(
    summary="Simplistic Get",
    tags=[
        "test",
        "user",
        "sample"
    ],
    description="Proof of concept",
    parameters=[
        swagger.PathParameter(
            name="id",
            description="root id",
            allow_empty_value=True,
            schema=swagger.Schema(
                type="string",
                format="email",
            )
        ),
        swagger.QueryParameter(
            name="age",
            description="age of user",
        ),
    ],
    responses=swagger.ResponsesObject()
)

servers = [
    swagger.Server(
        url="https://{sample}.sample/com",
        description="Test Suite",
        variables=dict(
            sample=swagger.ServerVariable(
                default="api",
                enum=[
                    "api",
                    "api2",
                    "api3"
                ],
            ),
        )
    ),
]


@swagger.Tag(name="getEcho", description="Retrieve echos wit Get")
@swagger.GET(
    tags=["getEcho"],
    operation_id="getEcho",
    parameters=[
        swagger.PathParameter(
            name="sample",
            schema=flaskdoc.String()
        )
    ],
    description="Retrieve echos wit Get",
    responses=swagger.ResponsesObject(
        responses={
            "200": swagger.ResponseObject(
                description="Success",
                content={
                    "text/plain": swagger.MediaType(
                        schema=flaskdoc.Email()
                    )
                }
            )
        }
    ),
)
@blp.route("/echo/<string:sample>", methods=["GET"])
def echo(sample: str):
    """
    Sample GET request
    Returns: Echos back whatever was sent

    """
    return sample


@swagger.Tag(name="postEcho", description="Posts an Echo")
@swagger.POST(tags=["postEcho"], description="Posts an Echo", responses=swagger.ResponsesObject())
@blp.route("/echo", methods=["POST"])
def post():
    req = flask.request.get_json(force=True)
    return flask.jsonify(req), 200


# @swagger.Tag(name="first")
# @swagger.Tag(name="second")
# @swagger.Tag(name="third")
def pest(ar):
    print(ar)


if __name__ == '__main__':
    pest(ar=34)
    pest(ar=134)
