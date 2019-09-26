import flask
import flaskdoc
from swagger import GET, PathParameter, Server, ServerVariable

blp = flaskdoc.Blueprint("Dummy", __name__)


@blp.route("/echo/<sample>",
           ref="Simplistic",
           description="Test API Summary",
           methods=GET(
               summary="TEST",
               tags=["Pets", "Snakes"],
               description="Howdy API Test",
               parameters=[
                   PathParameter(name="sample",
                                 description="Useless parameter")
               ]
           ),
           servers=[
               Server(url="https://{sample}.sample/com",
                      description="Test Suite",
                      variables=dict(
                          sample=ServerVariable(default_val="api",
                                                enum_values=["api", "api2", "api3"])
                      ))
           ]
           )
def get(sample):
    """
    Sample GET request
    Returns:

    """
    return "Echo"


@blp.route("/post", ref="Sponsors Cove", description="Howdy for post", methods=["GET"])
def post():
    return flask.jsonify(dict(a="Test", message="Success")), 200
