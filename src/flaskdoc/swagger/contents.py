import attr


@attr.s
class Content(object):
    """ A content container for response and request objects """

    content_type = attr.ib(type=str)
    schema = attr.ib(type=type)
    description = attr.ib(default=None, type=str)


@attr.s
class JsonType(Content):
    content_type = attr.ib(default="application/json", init=False)


@attr.s
class PlainText(Content):
    content_type = attr.ib(default="text/plain", init=False)
