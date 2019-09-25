from flaskdoc.swagger.core import SwaggerBase, SwaggerDict
from flaskdoc.swagger.parameters import Style


class Content(SwaggerBase):

    def __init__(self):
        super(Content, self).__init__()
        self.contents = SwaggerDict()

    def add_media_type(self, name, media_type):
        self.contents[name] = media_type.as_dict()

    def as_dict(self):
        return self.contents


class MediaType(SwaggerBase):
    """ Each Media Type Object provides schema and examples for the media type identified by its key. """

    def __init__(self):
        super(MediaType, self).__init__()

        self.schema = None
        self.example = None
        self.examples = {}
        self.encoding = {}

    def add_exmple(self, name, example):
        self.examples[name] = example

    def add_eencoding(self, name, encoding):
        self.encoding[name] = encoding


class Encoding(SwaggerBase):
    """ A single encoding definition applied to a single schema property. """

    def __init__(self, content_type, headers=None, style=None, explode=None, allow_reserved=False):
        super(Encoding, self).__init__()
        self.content_type = content_type
        self.headers = headers
        self._style = style if isinstance(style, Style) else Style(style)
        self.explode = explode
        self.allow_reserved = allow_reserved

    @property
    def style(self):
        return self._style.value

    def add_header(self, name, header):
        self.headers[name] = header


class Header(SwaggerBase):

    def __init__(self, required=False,
                 description=None,
                 deprecated=False,
                 allow_empty_value=False,
                 explode=False,
                 allow_reserved=False,
                 schema=None,
                 content=None,
                 example=None,
                 examples=None):
        super(Header, self).__init__()
        self.description = description
        self.deprecated = deprecated

        self.allow_empty_value = allow_empty_value
        self.allow_reserved = allow_reserved
        self.schema = schema
        self.content = content

        self.explode = explode
        self._required = required
        self._style = Style.SIMPLE
        self.example = example
        self.examples = examples

    @property
    def required(self):
        return self._required

    @property
    def style(self):
        return self._style

    def as_dict(self):
        d = SwaggerDict()
        d["description"] = self.description
        d["required"] = self.required
        d["deprecated"] = self.deprecated
        d["allowEmptyValue"] = self.allow_empty_value
        d["style"] = self.style.value if self.style else None
        d["explode"] = self.explode
        d["allowReserved"] = self.allow_reserved
        d["content"] = self.content.as_dict() if self.content else None
        d.update(super(Header, self).as_dict())
        return d


class ExternalDocumentation(SwaggerBase):
    """ Allows referencing an external resource for extended documentation. """

    def __init__(self, url, description=None):
        super(ExternalDocumentation, self).__init__()
        self.url = url
        self.description = description


class Example(SwaggerBase):

    def __init__(self, summary=None, description=None, value=None, external_value=None):
        super(Example, self).__init__()

        self.summary = summary
        self.description = description
        self.value = value
        self.external_value = external_value


class Link(SwaggerBase):
    """
    The Link object represents a possible design-time link for a response. The presence of a link does not guarantee
    the caller's ability to successfully invoke it, rather it provides a known relationship and traversal mechanism
    between responses and other operations. Unlike dynamic links (i.e. links provided in the response payload),
    the OAS linking mechanism does not require link information in the runtime response. For computing links,
    and providing instructions to execute them, a runtime expression is used for accessing values in an operation and
    using them as parameters while invoking the linked operation.
    """

    def __init__(self):
        super(Link, self).__init__()
        self.operation_ref = None
        self.operation_id = None
        self.description = None
