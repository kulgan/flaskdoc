import flask

from flaskdoc import swagger
from flaskdoc.examples.link_example import specs

api = flask.Blueprint("link-example", __name__, url_prefix="/link-example")

info = swagger.Info(title="Link Example", version="1.0.0")

links = {
    "UserRepositories": swagger.Link(
        operation_id="getRepositoriesByName", parameters={"username": "$response.body#/username"}
    ),
    "UserRepository": swagger.Link(
        operation_id="getRepository",
        parameters={"username": "$response.body#/username", "slug": "$response.body#/slug"},
    ),
    "RepositoryPullRequests": swagger.Link(
        operation_id="getPullRequestByRepository",
        parameters={"username": "#response.body#/owner/username", "slug": "$response.body#/slug"},
    ),
    "PullRequestMerge": swagger.Link(
        operation_id="mergePullRequest",
        parameters={
            "username": "$response.body#/author/username",
            "slug": "$response.body#/repository/slug",
            "pid": "$response.body#/id",
        },
    ),
}


@specs.get_user_by_name
@api.route("/2.0/users/<string:username>", methods=["GET"])
def get_user_by_name(username):
    pass


@specs.get_repository_by_owner
@api.route("/2.0/repositories/<string:username>", methods=["GET"])
def get_repository_by_owner(username):
    pass


@specs.get_repository
@api.route("/2.0/repositories/<string:username>/<string:slug>", methods=["GET"])
def get_repository(username, slug):
    pass


@specs.get_pull_requests_by_repository
@api.route("/2.0/repositories/<string:username>/<string:slug>/pullrequests", methods=["GET"])
def get_pull_requests_by_repository(username, slug):
    pass


@specs.get_pull_requests_by_id
@api.route(
    "/2.0/repositories/<string:username>/<string:slug>/pullrequests/<string:pid>", methods=["GET"]
)
def get_pull_requests_by_id(username, slug, pid):
    pass


@specs.merge_pull_request
@api.route(
    "/2.0/repositories/<string:username>/<string:slug>/pullrequests/<string:pid>/merge",
    methods=["POST"],
)
def merge_pull_request(username, slug, pid):
    pass
