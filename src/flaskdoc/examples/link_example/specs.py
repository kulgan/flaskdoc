from flaskdoc import swagger
from flaskdoc.examples.link_example import schemas

get_user_by_name = swagger.GET(
    operation_id="getUserByName",
    parameters=[swagger.PathParameter(name="username", schema=str)],
    responses={
        "200": swagger.ResponseObject(
            description="The User",
            content=swagger.JsonType(schema=schemas.User),
            links={"userRepositories": swagger.LinkReference("UserRepositories")},
        )
    },
)

get_repository_by_owner = swagger.GET(
    operation_id="getRepositoryByOwner",
    parameters=[swagger.PathParameter(name="username", schema=str)],
    responses={
        "200": swagger.ResponseObject(
            description="repositories owned by the supplied user",
            content=swagger.JsonType(schema=[schemas.Repository]),
            links={"userRepository": swagger.LinkReference("UserRepository")},
        )
    },
)


get_repository = swagger.GET(
    operation_id="getRepository",
    parameters=[
        swagger.PathParameter(
            name="username",
            schema=str,
        ),
        swagger.PathParameter(name="slug", schema=str),
    ],
    responses={
        "200": swagger.ResponseObject(
            description="The repository",
            content=swagger.JsonType(schema=schemas.Repository),
            links={"repositoryPullRequest": swagger.LinkReference("RepositoryPullRequest")},
        ),
    },
)


get_pull_requests_by_repository = swagger.GET(
    operation_id="getPullRequestByRepository",
    parameters=[
        swagger.PathParameter(
            name="username",
            schema=str,
        ),
        swagger.PathParameter(name="slug", schema=str),
        swagger.QueryParameter(name="state", schema=schemas.RepositoryState),
    ],
    responses={
        "200": swagger.ResponseObject(
            description="an array of pull request objects",
            content=swagger.JsonType(schema=[schemas.PullRequest]),
        )
    },
)


get_pull_requests_by_id = swagger.GET(
    operation_id="getPullRequestsById",
    parameters=[
        swagger.PathParameter(
            name="username",
            schema=str,
        ),
        swagger.PathParameter(name="slug", schema=str),
        swagger.PathParameter(name="pid", schema=str),
    ],
    responses={
        "200": swagger.ResponseObject(
            description="an array of pull request objects",
            content=swagger.JsonType(schema=[schemas.PullRequest]),
            links={"pullRequestMerge": swagger.LinkReference("PullRequestMerge")},
        ),
    },
)

merge_pull_request = swagger.POST(
    operation_id="mergePullRequest",
    parameters=[
        swagger.PathParameter(
            name="username",
            schema=str,
        ),
        swagger.PathParameter(name="slug", schema=str),
        swagger.PathParameter(name="pid", schema=str),
    ],
    responses={"204": swagger.ResponseObject(description="This PR was successfully merged")},
)
