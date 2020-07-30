from enum import Enum

from flaskdoc import jo, swagger


@jo.schema()
class ApiResponse(object):
    code = jo.integer()
    type = jo.string()
    message = jo.string()


@jo.schema()
class Category(object):
    id = jo.integer(format="int64")
    name = jo.string()


class Status(Enum):
    """ Pet status in the store """

    available = "available"
    pending = "pending"
    sold = "sold"


@jo.schema()
class Tag(object):
    id = jo.integer(format="int64")
    name = jo.string()


@jo.schema()
class Pet(object):
    id = jo.integer(format="int64")
    category = jo.object(item=Category)
    name = jo.string(required=True, example="doggie")
    photo_urls = jo.array(item=str, required=True)
    status = jo.object(item=Status)
    tags = jo.array(item=Tag)


@jo.schema()
class Order(object):
    id = jo.integer(format="int64")
    pet_id = jo.integer(format="int64")
    quantity = jo.integer(format="int32")
    ship_date = jo.string(format="date-time")
    status = jo.object(item=Status, description="Order Status")
    complete = jo.boolean()


@jo.schema()
class User(object):
    id = jo.integer(format="int64")
    username = jo.string()
    first_name = jo.string()
    last_name = jo.string()
    email = jo.email()
    password = jo.string()
    phone = jo.string()
    user_status = jo.integer(format="int32", description="User status")


upload_image_spec = swagger.POST(
    tags=["pet"],
    summary="uploads an image",
    operation_id="uploadFile",
    parameters=[
        swagger.PathParameter(name="petId", description="ID of pet to update", schema=jo.Int64())
    ],
    request_body=swagger.RequestBody(
        content=jo.Content(
            content_type="multipart/form-data",
            schema=jo.Schema(
                properties=dict(
                    file=jo.BinaryString(description="file to upload"),
                    additional_metadata=jo.String(
                        description="additional data to pass to server"
                    ),
                )
            ),
        )
    ),
    responses={
        "200": swagger.ResponseObject(
            description="successful operation", content=jo.JsonType(schema=ApiResponse)
        )
    },
    security=[{"petstoreAuth": ["write:pets", "read:pets"]}],
)


update_pet_spec = swagger.PUT(
    tags=["pet"],
    summary="Update an existing pet",
    operation_id="updatePet",
    request_body=swagger.RequestBody(
        content=[jo.JsonType(schema=Pet), jo.XmlType(schema=Pet)], required=True,
    ),
    responses={
        "400": swagger.ResponseObject(description="Invalid ID supplied"),
        "404": swagger.ResponseObject(description="Pet not found"),
        "405": swagger.ResponseObject(description="Validation exception"),
    },
    security=[{"petstoreAuth": ["write:pets", "read:pets"]}],
)


add_pet_spec = swagger.POST(
    tags=["pet"],
    summary="Add a new pet to the store",
    operation_id="addPet",
    request_body=swagger.RequestBody(
        content=[jo.JsonType(schema=Pet), jo.XmlType(schema=Pet)], required=True,
    ),
    responses={"405": swagger.ResponseObject(description="Invalid input")},
    security=[{"petStoreAuth": ["write:pets", "read:pets"]}],
)


find_by_status_spec = swagger.GET(
    tags=["pet"],
    summary="Finds Pets by status",
    description="Multiple status values can be provided with comma separated strings",
    operation_id="findPetsByStatus",
    parameters=[
        swagger.QueryParameter(
            name="status",
            explode=True,
            required=True,
            description="Status values need to be considered for filter",
            schema=jo.Array(items=jo.String(enum=Status._member_names_, default="available")),
        )
    ],
    responses={
        "200": swagger.ResponseObject(
            description="Successful operation",
            content=[
                jo.JsonType(schema=jo.Array(items=Pet)),
                jo.XmlType(schema=jo.Array(items=Pet)),
            ],
        ),
        "400": swagger.ResponseObject(description="Invalid status value"),
    },
    security=[{"petstoreAuth": ["write:pets", "read:pets"]}],
)

find_by_tags_spec = swagger.GET(
    tags=["pet"],
    summary="Finds Pets by tags",
    description="Multiple tags can be provided with comma separated strings. Use tag1, tag2, tag3 for testing",
    operation_id="findPetsByTags",
    parameters=[
        swagger.QueryParameter(
            name="tags",
            explode=True,
            required=True,
            description="Status values need to be considered for filter",
            schema=jo.Array(items=str),
        )
    ],
    responses={
        "200": swagger.ResponseObject(
            description="Successful operation",
            content=[
                jo.JsonType(schema=jo.Array(items=Pet)),
                jo.XmlType(schema=jo.Array(items=Pet)),
            ],
        ),
        "400": swagger.ResponseObject(description="Invalid status value"),
    },
    security=[{"petstoreAuth": ["write:pets", "read:pets"]}],
)


get_by_id_spec = swagger.GET(
    tags=["pet"],
    summary="Find pet by ID",
    description="Returns a single pet",
    operation_id="getPetById",
    parameters=[
        swagger.PathParameter(name="petId", description="ID of pet to return", schema=jo.Int64(),)
    ],
    responses={
        "200": swagger.ResponseObject(
            description="Successful operation",
            content=[
                jo.JsonType(schema=jo.Array(items=Pet)),
                jo.XmlType(schema=jo.Array(items=Pet)),
            ],
        ),
        "400": swagger.ResponseObject(description="Invalid ID supplied"),
        "404": swagger.ResponseObject(description="Pet not found"),
    },
    security=[{"apiKey": [""]}],
)


update_by_id_spec = swagger.POST(
    tags=["pet"],
    summary="Updates a pet in the store with form data",
    operation_id="updatePetWithForm",
    parameters=[
        swagger.PathParameter(
            name="petId", description="ID of pet that needs to be updated", schema=jo.Int64(),
        )
    ],
    request_body=swagger.RequestBody(
        content=jo.Content(
            content_type="application/x-www-form-urlencoded",
            schema=jo.Schema(
                properties=dict(
                    name=jo.String(description="Updated name of the pet"),
                    status=jo.String(description="Updated status of the pet",),
                )
            ),
        )
    ),
    responses={"405": swagger.ResponseObject(description="Invalid input")},
    security=[{"petstoreAuth": ["write:pets", "read:pets"]}],
    deprecated=True,
)


delete_by_id_spec = swagger.DELETE(
    tags=["pet"],
    summary="Deletes a pet",
    operation_id="deletePet",
    parameters=[
        swagger.HeaderParameter(name="api_key", schema=jo.String()),
        swagger.PathParameter(
            name="petId", description="ID of pet that needs to be updated", schema=jo.Int64(),
        ),
    ],
    responses={
        "400": swagger.ResponseObject(description="Invalid ID supplied"),
        "404": swagger.ResponseObject(description="Pet not found"),
    },
    security=[{"petstoreAuth": ["write:pets", "read:pets"]}],
)


place_order_spec = swagger.POST(
    tags=["store"],
    summary="Place an order for a pet",
    operation_id="placeOrder",
    request_body=swagger.RequestBody(
        description="order placed for purchasing the pet",
        content=jo.JsonType(schema=Order),
        required=True,
    ),
    responses={
        "200": swagger.ResponseObject(
            description="successful operation",
            content=[jo.JsonType(schema=Order), jo.XmlType(schema=Order)],
        ),
        "400": swagger.ResponseObject(description="Invalid ID supplied"),
    },
)


get_order_by_id_spec = swagger.GET(
    tags=["store"],
    summary="Find purchase order by ID",
    description="For valid response try integer IDs with value >+ 1 and <= 10. Other values will generate exceptions",
    operation_id="getOrderById",
    parameters=[swagger.PathParameter(name="orderId", schema=jo.Int64(maximum=10, minimum=1))],
    responses={
        "200": swagger.ResponseObject(
            description="successful operation",
            content=[jo.JsonType(schema=Order), jo.XmlType(schema=Order)],
        ),
        "400": swagger.ResponseObject(description="Invalid ID supplied"),
        "404": swagger.ResponseObject(description="Order not found"),
    },
)


delete_order_by_id_spec = swagger.DELETE(
    tags=["store"],
    summary="Delete purchase order by ID",
    description="For valid response try integer IDs with positive integer value. "
    "Negative or non-integer values will generat API errors",
    operation_id="deleteOrder",
    parameters=[swagger.PathParameter(name="orderId", schema=jo.Int64(maximum=10, minimum=1))],
    responses={
        "400": swagger.ResponseObject(description="Invalid ID supplied"),
        "404": swagger.ResponseObject(description="Order not found"),
    },
)


order_inventory_spec = swagger.GET(
    tags=["store"],
    summary="Returns a map of status codes to quantities",
    operation_id="getInventory",
    responses={
        "200": swagger.ResponseObject(
            description="successful operation",
            content=jo.JsonType(schema=jo.Object(additional_properties=jo.Integer())),
        )
    },
    security=[{"apiKey": [""]}],
)


create_with_array_spec = swagger.POST(
    tags=["user"],
    summary="Creates list off users with given input array",
    operation_id="createUsersWithArrayInput",
    request_body=swagger.RequestBody(
        description="List of user object",
        content=jo.JsonType(schema=jo.Array(items=User)),
        required=True,
    ),
    responses={"200": swagger.ResponseObject(description="successful operation")},
)


create_with_list_spec = swagger.POST(
    tags=["user"],
    summary="Creates list off users with given input array",
    operation_id="createUsersWithListInput",
    request_body=swagger.RequestBody(
        description="List of user object",
        content=jo.JsonType(schema=jo.Array(items=User)),
        required=True,
    ),
    responses={"200": swagger.ResponseObject(description="successful operation")},
)


get_by_username_spec = swagger.GET(
    tags=["user"],
    summary="Get user by user name",
    operation_id="getUserByName",
    parameters=[
        swagger.PathParameter(
            name="username",
            description="The name that needs to be fetched, Use user1 for testing.",
            schema=jo.String(),
        )
    ],
    responses={
        "200": swagger.ResponseObject(
            description="successful operation",
            content=[jo.JsonType(schema=User), jo.XmlType(schema=User)],
        ),
        "400": swagger.ResponseObject(description="Invalid username supplied"),
        "404": swagger.ResponseObject(description="User not found"),
    },
)

update_user_spec = swagger.PUT(
    tags=["user"],
    summary="Updated user",
    description="This can only be done by the logged in user.",
    parameters=[
        swagger.PathParameter(
            name="username",
            description="The name that needs to be fetched, Use user1 for testing.",
            schema=jo.String(),
        )
    ],
    request_body=swagger.RequestBody(
        description="Updated user object", content=jo.JsonType(User),
    ),
    responses={
        "400": swagger.ResponseObject(description="Invalid ID supplied"),
        "404": swagger.ResponseObject(description="Order not found"),
    },
)


delete_user_by_username_spec = swagger.DELETE(
    tags=["user"],
    summary="Delete user",
    description="this can only be done by the logged in user.",
    operation_id="deleteUser",
    parameters=[
        swagger.PathParameter(
            name="username",
            description="The name that needs to be fetched, Use user1 for testing.",
            schema=jo.String(),
        )
    ],
    responses={
        "400": swagger.ResponseObject(description="Invalid ID supplied"),
        "404": swagger.ResponseObject(description="Order not found"),
    },
)


login_spec = swagger.GET(
    tags=["user"],
    summary="Logs user into the system",
    operation_id="loginUser",
    parameters=[
        swagger.QueryParameter(
            name="username",
            description="The name that needs to be fetched, Use user1 for testing.",
            schema=jo.String(),
        ),
        swagger.QueryParameter(
            name="password",
            description="The password for login in clear text",
            required=True,
            schema=jo.String(),
        ),
    ],
    responses={
        "200": swagger.ResponseObject(
            description="successful operation",
            headers={
                "X-Rate-Limit": swagger.Header(
                    description="calls oer hour allowed by user", schema=jo.Integer()
                ),
                "X-Expires-After": swagger.Header(
                    description="date in UTC when token expires",
                    schema=jo.String(format="date-time"),
                ),
            },
            content=[jo.JsonType(schema=str), jo.XmlType(schema=str)],
        ),
        "400": swagger.ResponseObject(description="Invalid username/password supplied"),
    },
)
