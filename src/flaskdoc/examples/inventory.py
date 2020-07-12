import attr
import flask

import flaskdoc.schema
from flaskdoc import swagger

blp = flask.Blueprint("inventory", __name__, url_prefix="/inventory")


@attr.s
class Manufacturer(object):
    name = attr.ib(type=str)
    phone = attr.ib(default=None, type=str)
    homepage = attr.ib(default=None, type=str)


@attr.s
class InventoryItem(object):
    id = attr.ib(type=str)
    name = attr.ib(type=str)
    manufacturer = attr.ib(type=Manufacturer)
    release_date = attr.ib(type=str)


search_inventory_docs = swagger.GET(
    tags=["developers"],
    operation_id="searchInventory",
    summary="searches inventory",
    description="By passing in the appropriate options, you can search for available inventory in the system",
    parameters=[
        swagger.QueryParameter(
            required=False,
            name="searchString",
            schema=str,
            description="pass an optional search string for looking up inventory",
        ),
        swagger.QueryParameter(
            name="skip", schema=int, description="number of records to skip for pagination",
        ),
        swagger.QueryParameter(
            name="limit",
            schema=flaskdoc.Int32(maximum=50),
            description="maximum number of records to return",
        ),
    ],
    responses={
        "200": swagger.ResponseObject(
            description="search results matching criteria",
            content=flaskdoc.schema.JsonType(schema=[InventoryItem]),
        ),
        "400": swagger.ResponseObject(description="bad input parameter"),
    },
)


add_inventory_docs = swagger.POST(
    tags=["admin"],
    operation_id="addInventory",
    summary="adds an inventory item",
    description="adds an item to the system",
    request_body=swagger.RequestBody(
        content=flaskdoc.schema.JsonType(schema=InventoryItem),
        description="Inventory item to add",
    ),
    responses={
        "201": swagger.ResponseObject(description="item created"),
        "400": swagger.ResponseObject(description="Invalid input, object invalid"),
        "409": swagger.ResponseObject(description="an existing item already exists"),
    },
)


@search_inventory_docs
@blp.route("", methods=["GET"])
def search_inventory():
    pass


@add_inventory_docs
@blp.route("", methods=["POST"])
def add_inventory():
    pass
