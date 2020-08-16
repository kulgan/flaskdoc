import enum

from flaskdoc import jo


@jo.schema()
class User(object):
    username = jo.string()
    uuid = jo.string(str_format="uuid")


@jo.schema()
class Repository(object):
    slug = jo.string()
    owner = jo.object(item=User)


@jo.schema()
class PullRequest(object):
    id = jo.integer()
    title = jo.string()
    repository = jo.object(item=Repository)
    author = jo.object(item=User)


class RepositoryState(enum.Enum):

    open = "open"
    merged = "merged"
    declined = "declined"
