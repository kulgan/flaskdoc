import flask

import flaskdoc
from flaskdoc import swagger

blp = flask.Blueprint("inventory", __name__, url_prefix="/inventory")


class InventoryItem:
    pass


search_inventory_docs = swagger.GET(
    tags=["developers"],
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


add_inventory_docs = swagger.POST(
    tags=["admin"],
    operation_id="addInventory",
    summary="adds an inventory item",
    description="adds an item to the system",
    request_body=swagger.RequestBody(
        content={"application/json": InventoryItem}, description="Inventory item to add",
    ),
    responses=swagger.ResponsesObject(
        responses={
            "201": swagger.ResponseObject(description="item created"),
            "400": swagger.ResponseObject(description="Invalid input, object invalid",),
            "409": swagger.ResponseObject(description="an existing item already exists"),
        }
    ),
)


@search_inventory_docs
@blp.route("", methods=["GET"])
def search_inventory():
    pass


@add_inventory_docs
@blp.route("", methods=["POST"])
def add_inventory():
    pass
