from flaskdoc.swagger import SwaggerBase


class Path(SwaggerBase):

    def __init__(self):
        super(Path, self).__init__()
        self._items = {}

    def add_path_item(self, name, path_item):
        self._items[name] = path_item


class PathItem(SwaggerBase):

    def __init__(self):
        super(PathItem, self).__init__()

        self.ref = None
        self.summary = None
        self.description = None

        self.servers = []

        self.get = None  # type -> Operation
        self.delete = None  # type -> Operation
        self.head = None  # type -> Operation
        self.options = None  # type -> Operation
        self.patch = None  # type -> Operation
        self.post = None  # type -> Operation
        self.put = None  # type -> Operation
        self.trace = None  # type -> Operation


class Operation(SwaggerBase):
    
    def __init__(self, responses):
        super(Operation, self).__init__()
        self.responses = responses
        self.tags = []

        self.deprecated = False
