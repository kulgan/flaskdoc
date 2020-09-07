import flask

from flaskdoc import swagger
from flaskdoc.examples.uspto import spec

api = flask.Blueprint("uspto", __name__, url_prefix="/uspto")

servers = [
    swagger.Server(
        url="{scheme}://developer.uspto.gov/ds-api",
        variables={
            "scheme": swagger.ServerVariable(
                description="The Data Set API is accessible via https and http",
                enum=["http", "https"],
                default="https",
            )
        },
    )
]

info = swagger.Info(
    description="""The Data Set API (DSAPI) allows the public users to discover and search USPTO exported data sets.
    This is a generic API that allows USPTO users to make any CSV based data files searchable through API. With the
    help of GET call, it returns the list of data fields that are searchable. With the help of POST call, data can be
    fetched based on the filters on the field names. Please note that POST call is used to search the actual data.
    The reason for the POST call is that it allows users to specify any complex search criteria without worry about
    the GET size limitations as well as encoding of the input parameters.""",
    version="1.0.0",
    title="USPTO Data Set API",
    contact=swagger.Contact(
        name="Open Data Portal", url="https://developer.uspto.gov", email="developer@uspto.gov"
    ),
)

tags = [
    swagger.Tag(name="metadata", description="Find out about the data sets"),
    swagger.Tag(name="search", description="Search a data set"),
]


@spec.list_available
@api.route("/")
def list_available():
    return flask.jsonify([])


@spec.get_info
@api.route("/<string:dataset>/<string:version>/fields")
def get_info(dataset, version):
    pass
