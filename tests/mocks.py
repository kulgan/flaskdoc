import flaskdoc

blp = flaskdoc.Blueprint("Dummy", __name__)


@blp.route("/echo", tags=["test"], description="Test API Summary", methods=["GET"])
def echo():
    return "Echo"
