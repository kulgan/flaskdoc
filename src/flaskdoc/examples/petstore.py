import flask

from flaskdoc import swagger
from flaskdoc.examples.petstore_specs import (
    Pet,
    add_pet_spec,
    create_user_spec,
    create_with_array_spec,
    create_with_list_spec,
    delete_by_id_spec,
    delete_order_by_id_spec,
    delete_user_by_username_spec,
    find_by_status_spec,
    find_by_tags_spec,
    get_by_id_spec,
    get_by_username_spec,
    get_order_by_id_spec,
    login_spec,
    logout_spec,
    order_inventory_spec,
    place_order_spec,
    update_by_id_spec,
    update_pet_spec,
    update_user_spec,
    upload_image_spec,
)

pet = flask.Blueprint("pet", __name__, url_prefix="/pet")
store = flask.Blueprint("store", __name__, url_prefix="/store")
user = flask.Blueprint("user", __name__, url_prefix="/user")
info = swagger.Info(
    title="Swagger Petstore",
    version="1.0.5",
    description="This is a sample server Petstore server.  You can find out more about Swagger at ["
    "http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger]("
    "http://swagger.io/irc/).  For this sample, you can use the api key `special-key` to test the "
    "authorization filters.",
    contact=swagger.Contact(
        email="apiteam@swagger.io",
    ),
    license=swagger.License(
        name="Apache 2.0",
        url="http://www.apache.org/licenses/LICENSE-2.0.html",
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
    "api_key": swagger.ApiKeySecurityScheme(name="api_key"),
    "petstore_auth": swagger.OAuth2SecurityScheme(
        flows=swagger.ImplicitOAuthFlow(
            authorization_url="https://petstore.swagger.io/oauth/authorize",
            scopes={"read:pets": "read your pets", "write:pets": "write pets in your account"},
        )
    ),
}


@upload_image_spec
@pet.route("/<int:petId>/uploadImage", methods=["POST"])
def upload_image(petId):
    pass


@update_pet_spec
@pet.route("", methods=["PUT"])
def update_pet():
    pass


@add_pet_spec
@pet.route("", methods=["POST"])
def add_pet():
    pass


@find_by_status_spec
@pet.route("/findByStatus", methods=["GET"])
def find_by_status():
    return flask.jsonify([Pet(name="high")])


@find_by_tags_spec
@pet.route("/findByTags", methods=["GET"])
def find_by_tags():
    pass


@get_by_id_spec
@update_by_id_spec
@delete_by_id_spec
@pet.route("/<int:petId>", methods=["GET", "POST", "DELETE"])
def by_id(petId):
    pass


@place_order_spec
@store.route("/order", methods=["POST"])
def place_order():
    pass


@get_order_by_id_spec
@delete_order_by_id_spec
@store.route("/order/<int:orderId>", methods=["GET", "DELETE"])
def order_by_id(orderId):
    pass


@order_inventory_spec
@store.route("/inventory", methods=["GET"])
def get_inventory():
    pass


@create_with_array_spec
@user.route("/createWithArray", methods=["POST"])
def create_users_with_array():
    pass


@create_with_list_spec
@user.route("/createWithList", methods=["POST"])
def create_users_with_list():
    pass


@delete_user_by_username_spec
@get_by_username_spec
@update_user_spec
@user.route("/<string:username>", methods=["GET", "PUT", "DELETE"])
def by_username(username):
    pass


@login_spec
@user.route("/login", methods=["GET"])
def login():
    pass


@logout_spec
@user.route("/logout", methods=["GET"])
def logout():
    pass


@create_user_spec
@user.route("", methods=["POST"])
def create_user():
    pass
