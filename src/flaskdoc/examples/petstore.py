from enum import Enum

import flask

from flaskdoc import jo, swagger

pet = flask.Blueprint("petstore", __name__, url_prefix="/pet")
info = swagger.Info(
    title="Swagger Petstore",
    version="1.0.5",
    description="This is a sample server Petstore server.  You can find out more about Swagger at ["
    "http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger]("
    "http://swagger.io/irc/).  For this sample, you can use the api key `special-key` to test the "
    "authorization filters.",
    contact=swagger.Contact(email="apiteam@swagger.io",),
    license=swagger.License(
        name="Apache 2.0", url="http://www.apache.org/licenses/LICENSE-2.0.html",
    ),
    terms_of_service="http://swagger.io/terms/",
)
external_docs = swagger.ExternalDocumentation(
    description="Find out more about Swagger", url="http://swagger.io"
)
servers = [
    swagger.Server(url="https://petstore.swagger.io/v2"),
    swagger.Server(url="http://petstore.swagger.io/v2"),
]
tags = [
    swagger.Tag(
        name="pet",
        description="Everything about your Pets",
        external_docs=swagger.ExternalDocumentation(
            description="Find out more", url="http://swagger.io"
        ),
    ),
    swagger.Tag(name="store", description="Access to Petstore orders"),
    swagger.Tag(
        name="user",
        description="Operations about user",
        external_docs=swagger.ExternalDocumentation(
            description="Find out more about our store", url="http://swagger.io"
        ),
    ),
]

security_schemes = {
    "apikey": swagger.ApiKeySecurityScheme(name="apikey"),
    "petstore_auth": swagger.OAuth2SecurityScheme(
        flows=swagger.ImplicitOAuthFlow(
            authorization_url="https://petstore.swagger.io/oauth/authorize",
            scopes={"read:pets": "read your pets", "write:pets": "write pets in your account"},
        )
    ),
}


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


@swagger.POST(
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
@pet.route("/<int:petId>/uploadImage", methods=["POST"])
def upload_image(petId):
    pass


@swagger.PUT(
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
@pet.route("", methods=["PUT"])
def update_pet():
    pass


@swagger.POST(
    tags=["pet"],
    summary="Add a new pet to the store",
    operation_id="addPet",
    request_body=swagger.RequestBody(
        content=[jo.JsonType(schema=Pet), jo.XmlType(schema=Pet)], required=True,
    ),
    responses={"405": swagger.ResponseObject(description="Invalid input")},
    security=[{"petStoreAuth": ["write:pets", "read:pets"]}],
)
@pet.route("", methods=["POST"])
def add_pet():
    pass


@swagger.GET(
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
            schema=jo.Array(items=Status, default="available"),
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
@pet.route("/findByStatus", methods=["GET"])
def find_by_status():
    return flask.jsonify([Pet(name="high")])


@swagger.GET(
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
@pet.route("/findByTags", methods=["GET"])
def find_by_tags():
    pass


@swagger.GET(
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
    security=[{"apikey": []}],
)
@swagger.POST(
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
@swagger.DELETE(
    tags=["pet"],
    summary="Deletes a pet",
    operation_id="deletePet",
    parameters=[
        swagger.HeaderParameter(name="apikey", schema=jo.String(),),
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
@pet.route("/<int:petId>", methods=["GET", "POST"])
def get_by_id(petId):
    pass
