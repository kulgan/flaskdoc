import flask

from flaskdoc import jo, swagger

blp = flask.Blueprint("inventory", __name__, url_prefix="/inventory")
info = swagger.Info(
    title="Test",
    version="1.2.2",
    contact=swagger.Contact(
        name="Rowland", email="r.ogra@daemonmailer" "+++.com", url="https://github.com/kulgan"
    ),
    license=swagger.License(name="Apache 2.0", url="https://www.example.com/license"),
)
servers = [swagger.Server(url="http://localhost:15172")]
tags = [
    swagger.Tag(name="admin", description="Secured Admin-Only calls"),
    swagger.Tag(name="developers", description="Operations available to regular developers"),
]


@jo.schema()
class Manufacturer(object):
    name = jo.string(example="ACME Corporation", required=True)
    phone = jo.string(example="408-867-5309")
    homepage = jo.string(str_format="url", example="https://www.acme-corp.com")


@jo.schema(camel_case_props=True)
class InventoryItem(object):
    id = jo.string(
        str_format="uuid", example="d290f1ee-6c54-4b01-90e6-d701748f0851", required=True
    )
    name = jo.string(example="Widget Adapter", required=True)
    manufacturer = jo.object(item=Manufacturer, required=True)
    release_date = jo.string(
        str_format="date-time", example="2016-08-29T09:12:33.001Z", required=True
    )


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
            name="skip",
            schema=int,
            description="number of records to skip for pagination",
        ),
        swagger.QueryParameter(
            name="limit",
            schema=swagger.Integer(maximum=50),
            description="maximum number of records to return",
        ),
    ],
    responses={
        "200": swagger.ResponseObject(
            description="search results matching criteria",
            content=swagger.JsonType(schema=[InventoryItem]),
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
        content=swagger.JsonType(schema=InventoryItem),
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
