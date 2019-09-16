import collections

from flaskdoc.swagger.core import SwaggerBase


class Content(object):

    def __init__(self):
        self._contents = collections.OrderedDict()

    def add_media_type(self, name, media_type):
        self._contents[name] = media_type


class MediaType(SwaggerBase):

    def __init__(self):
        super(MediaType, self).__init__()

        self.schema = None
        self.example = None
        self.examples = None
        self.encoding = None
