import flask
from swagger import GET
from swagger import Tag

import flaskdoc

blp = flaskdoc.Blueprint("Dummy", __name__)


@blp.route("/echo",
           ref="Simplistic",
           description="Test API Summary",
           methods=GET(summary="TEST",
                       tags=["Pets", "Snakes"],
                       description="Howdy API Test"))
def get():
    """
    Sample GET request
    Returns:

    """
    return "Echo"


@blp.route("/post", ref="Sponsors Cove", description="Howdy for post", methods=["GET"])
def post():
    return flask.jsonify(dict(a="Test", message="Success")), 200
