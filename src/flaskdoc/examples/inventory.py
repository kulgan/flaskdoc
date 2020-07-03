import flask
import flaskdoc

from flaskdoc import swagger

inv = flask.Blueprint("inventory", __name__, url_prefix="/inventory")


class InventoryItem:
    pass


@swagger.GET(
    operation_id="searchInventory",
    summary="searches inventory",
    description="By passing in the appropriate options, you can search for available inventory in the system",
    parameters=[
        swagger.QueryParameter(
            required=False,
            name="searchString",
            schema=flaskdoc.String(),
            description="pass an optional search string for looking up inventory",
        ),
        swagger.QueryParameter(
            name="skip", schema=flaskdoc.Int32(), description="number of records to skip for pagination",
        ),
        swagger.QueryParameter(
            name="limit", schema=flaskdoc.Int32(maximum=50), description="maximum number of records to return",
        ),
    ],
    responses=swagger.ResponsesObject(
        responses={
            "200": swagger.ResponseObject(
                description="search results matching criteria",
                content={"application/json": flaskdoc.Array(items=InventoryItem)},
            ),
            "400": swagger.ResponseObject(description="bad input parameter"),
        }
    ),
)
@swagger.Tag(name="developers", description="Operations available to regular developers")
@inv.route("", methods=["GET"])
def search_inventory():
    pass


@inv.route("", methods=["POST"])
def add_inventory():
    pass
