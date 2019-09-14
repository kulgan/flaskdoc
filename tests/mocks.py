import flask

import flaskdoc
from swagger.paths import GET
from swagger.tag import Tag

blp = flaskdoc.Blueprint("Dummy", __name__)


@blp.route("/echo",
           description="Test API Summary",
           methods=GET(summary="TEST",
                       tags=[Tag("Pets")],
                       description="Howdy API Test"))
def get():
  return "Echo"


@blp.route("/post", tags=["post", "message"], description="Howdy for post", methods=["POST"])
def post():
  return flask.jsonify(dict(a="Test", message="Success")), 200
