from enum import Enum

from flaskdoc import jo, swagger


@jo.schema()
class ApiResponse(object):
    code = jo.integer()
    type = jo.string()
    message = jo.string()


@jo.schema(xml="Category")
class Category(object):
    id = jo.integer(int_format="int64")
    name = jo.string()


class Status(Enum):
    """Pet status in the store"""

    available = "available"
    pending = "pending"
    sold = "sold"


@jo.schema(xml="Tag")
class Tag(object):
    id = jo.integer(int_format="int64")
    name = jo.string()


@jo.schema(xml="Pet", camel_case_props=True)
class Pet(object):
    id = jo.integer(int_format="int64")
    category = jo.object(item=Category)
    name = jo.string(required=True, example="doggie")
    photo_urls = jo.array(
        item=swagger.String(xml="photoUrl"),
        required=True,
        xml=swagger.XML(wrapped=True),
    )
    status = jo.object(item=Status)
    tags = jo.array(item=Tag, xml=swagger.XML(wrapped=True))


@jo.schema(xml="Order", camel_case_props=True)
class Order(object):
    id = jo.integer(int_format="int64")
    pet_id = jo.integer(int_format="int64")
    quantity = jo.integer(int_format="int32")
    ship_date = jo.string(str_format="date-time")
    status = jo.object(item=Status, description="Order Status")
    complete = jo.boolean()


@jo.schema(xml="User", camel_case_props=True)
class User(object):
    id = jo.integer(int_format="int64")
    username = jo.string()
    first_name = jo.string()
    last_name = jo.string()
    email = jo.email()
    password = jo.string()
    phone = jo.string()
    user_status = jo.integer(int_format="int32", description="User status")


upload_image_spec = swagger.POST(
    tags=["pet"],
    summary="uploads an image",
    operation_id="uploadFile",
    parameters=[
        swagger.PathParameter(
            name="petId",
            description="ID of pet to update",
            schema=swagger.Int64(),
        )
    ],
    request_body=swagger.RequestBody(
        content=swagger.MediaType(
            content_type="multipart/form-data",
            schema=swagger.Schema(
                properties=dict(
                    file=swagger.BinaryString(description="file to upload"),
                    additional_metadata=swagger.String(
                        description="additional data to pass to server"
                    ),
                )
            ),
        )
    ),
    responses={
        "200": swagger.ResponseObject(
            description="successful operation",
            content=swagger.JsonType(schema=ApiResponse),
        )
    },
    security=[{"petstore_auth": ["write:pets", "read:pets"]}],
)


update_pet_spec = swagger.PUT(
    tags=["pet"],
    summary="Update an existing pet",
    operation_id="updatePet",
    request_body=swagger.RequestBody(
        content=[swagger.JsonType(schema=Pet), swagger.XmlType(schema=Pet)],
        required=True,
    ),
    responses={
        "400": swagger.ResponseObject(description="Invalid ID supplied"),
        "404": swagger.ResponseObject(description="Pet not found"),
        "405": swagger.ResponseObject(description="Validation exception"),
    },
    security=[{"petstore_auth": ["write:pets", "read:pets"]}],
    extensions={"x-codegen-request-body-name": "body"},
)


add_pet_spec = swagger.POST(
    tags=["pet"],
    summary="Add a new pet to the store",
    operation_id="addPet",
    request_body=swagger.RequestBody(
        content=[swagger.JsonType(schema=Pet), swagger.XmlType(schema=Pet)],
        required=True,
        extensions={"x-required": True},
    ),
    responses={"405": swagger.ResponseObject(description="Invalid input")},
    security=[{"petstore_auth": ["write:pets", "read:pets"]}],
    extensions={"x-codegen-request-body-name": "body"},
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
            schema=[swagger.String(enum=Status._member_names_, default="available")],
        )
    ],
    responses={
        "200": swagger.ResponseObject(
            description="Successful operation",
            content=[swagger.JsonType(schema=[Pet]), swagger.XmlType(schema=[Pet])],
        ),
        "400": swagger.ResponseObject(description="Invalid status value"),
    },
    security=[{"petstore_auth": ["write:pets", "read:pets"]}],
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
            schema=swagger.Array(items=str),
        )
    ],
    responses={
        "200": swagger.ResponseObject(
            description="Successful operation",
            content=[
                swagger.JsonType(schema=swagger.Array(items=Pet)),
                swagger.XmlType(schema=swagger.Array(items=Pet)),
            ],
        ),
        "400": swagger.ResponseObject(description="Invalid status value"),
    },
    security=[{"petstore_auth": ["write:pets", "read:pets"]}],
    deprecated=True,
)


get_by_id_spec = swagger.GET(
    tags=["pet"],
    summary="Find pet by ID",
    description="Returns a single pet",
    operation_id="getPetById",
    parameters=[
        swagger.PathParameter(
            name="petId",
            description="ID of pet to return",
            schema=swagger.Int64(),
        )
    ],
    responses={
        "200": swagger.ResponseObject(
            description="Successful operation",
            content=[
                swagger.JsonType(
                    schema=Pet,
                    example=Pet(
                        id=10456,
                        name="spidey",
                        status="pending",
                        category=Category(id=123, name="smoked"),
                    ),
                ),
                swagger.XmlType(schema=Pet),
            ],
        ),
        "400": swagger.ResponseObject(description="Invalid ID supplied"),
        "404": swagger.ResponseObject(description="Pet not found"),
    },
    security=[{"api_key": []}],
)


update_by_id_spec = swagger.POST(
    tags=["pet"],
    summary="Updates a pet in the store with form data",
    operation_id="updatePetWithForm",
    parameters=[
        swagger.PathParameter(
            name="petId",
            description="ID of pet that needs to be updated",
            schema=swagger.Int64(),
        )
    ],
    request_body=swagger.RequestBody(
        content=swagger.MediaType(
            content_type="application/x-www-form-urlencoded",
            schema=swagger.Schema(
                properties=dict(
                    name=swagger.String(description="Updated name of the pet"),
                    status=swagger.String(description="Updated status of the pet"),
                ),
                example={"name": "Sylvester Stallone", "status": "available"},
            ),
        )
    ),
    responses={"405": swagger.ResponseObject(description="Invalid input")},
    security=[{"petstore_auth": ["write:pets", "read:pets"]}],
)


delete_by_id_spec = swagger.DELETE(
    tags=["pet"],
    summary="Deletes a pet",
    operation_id="deletePet",
    parameters=[
        swagger.HeaderParameter(name="api_key", schema=swagger.String()),
        swagger.PathParameter(
            name="petId",
            description="ID of pet that needs to be updated",
            schema=swagger.Int64(),
            examples={
                "negative": swagger.Example(
                    summary="negative value", value=-100, description="deeper negative"
                )
            },
        ),
    ],
    responses={
        "400": swagger.ResponseObject(description="Invalid ID supplied"),
        "404": swagger.ResponseObject(description="Pet not found"),
    },
    security=[{"petstore_auth": ["write:pets", "read:pets"]}],
)


place_order_spec = swagger.POST(
    tags=["store"],
    summary="Place an order for a pet",
    operation_id="placeOrder",
    request_body=swagger.RequestBody(
        description="order placed for purchasing the pet",
        content=swagger.JsonType(schema=Order, examples={"order": Order()}),
        required=True,
    ),
    responses={
        "200": swagger.ResponseObject(
            description="successful operation",
            content=[swagger.JsonType(schema=Order), swagger.XmlType(schema=Order)],
        ),
        "400": swagger.ResponseObject(description="Invalid ID supplied"),
    },
)


get_order_by_id_spec = swagger.GET(
    tags=["store"],
    summary="Find purchase order by ID",
    description="For valid response try integer IDs with value >+ 1 and <= 10. Other values will generate exceptions",
    operation_id="getOrderById",
    parameters=[
        swagger.PathParameter(name="orderId", schema=swagger.Int64(maximum=10, minimum=1))
    ],
    responses={
        "200": swagger.ResponseObject(
            description="successful operation",
            content=[swagger.JsonType(schema=Order), swagger.XmlType(schema=Order)],
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
    parameters=[
        swagger.PathParameter(name="orderId", schema=swagger.Int64(maximum=10, minimum=1))
    ],
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
            content=swagger.JsonType(
                schema=swagger.Object(additional_properties=swagger.Integer())
            ),
        )
    },
    security=[{"api_key": []}],
)


create_with_array_spec = swagger.POST(
    tags=["user"],
    summary="Creates list off users with given input array",
    operation_id="createUsersWithArrayInput",
    request_body=swagger.RequestBody(
        description="List of user object",
        content=swagger.JsonType(schema=[User]),
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
        content=swagger.JsonType(schema=[User]),
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
            schema=swagger.String(),
        )
    ],
    responses={
        "200": swagger.ResponseObject(
            description="successful operation",
            content=[swagger.JsonType(schema=User), swagger.XmlType(schema=User)],
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
            schema=swagger.String(),
        )
    ],
    request_body=swagger.RequestBody(
        description="Updated user object",
        content=swagger.JsonType(User),
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
            schema=swagger.String(),
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
            schema=swagger.String(),
        ),
        swagger.QueryParameter(
            name="password",
            description="The password for login in clear text",
            required=True,
            schema=swagger.String(),
        ),
    ],
    responses={
        "200": swagger.ResponseObject(
            description="successful operation",
            headers={
                "X-Rate-Limit": swagger.Header(
                    description="calls oer hour allowed by user",
                    schema=swagger.Integer(),
                ),
                "X-Expires-After": swagger.Header(
                    description="date in UTC when token expires",
                    schema=swagger.String(format="date-time"),
                ),
            },
            content=[swagger.JsonType(schema=str), swagger.XmlType(schema=str)],
        ),
        "400": swagger.ResponseObject(description="Invalid username/password supplied"),
    },
)


logout_spec = swagger.GET(
    tags=["user"],
    summary="Logs out current logged in user session",
    operation_id="logoutUser",
    responses=swagger.ResponsesObject(
        default=swagger.ResponseObject(description="successful operation")
    ),
)


create_user_spec = swagger.POST(
    tags=["user"],
    summary="Create user",
    description="This can only be done by the logged in user",
    operation_id="createUser",
    request_body=swagger.RequestBody(
        description="Created user object",
        content=swagger.JsonType(schema=User),
        required=True,
    ),
    responses=swagger.ResponsesObject(
        default=swagger.ResponseObject(description="successful operation")
    ),
)
