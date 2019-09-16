import enum

import swagger.core


class HttpMethod(enum.Enum):

  DELETE = "DELETE"
  HEAD = "HEAD"
  GET = "GET"
  OPTIONS = "OPTIONS"
  PATCH = "patch"
  POST = "POST"
  PUT = "PUT"
  TRACE = "TRACE"


class Paths(swagger.core.SwaggerBase):
  """ Paths collection used internally to aggregate all current path """

  def __init__(self, path_items=None):
    super(Paths, self).__init__()
    self._items = path_items

  def add_path_item(self, name, path_item):
    """
    Adds a path item
    Args:
      name (str): path url name, eg `/echo`
      path_item (PathItem) : PathItem instance describing the path
    """
    if not self._items:
      self._items = swagger.core.SwaggerDict()
    self._items[name] = path_item

  def as_dict(self):
    d = swagger.core.SwaggerDict()
    for k, v in self._items.items():
      d[k] = v.as_dict()
    d.update(super(Paths, self).as_dict())
    return d


class PathItem(swagger.core.SwaggerBase):

  def __init__(self, ref=None, summary=None, description=None):
    super(PathItem, self).__init__()

    self.ref = ref
    self.summary = summary
    self.description = description

    self.servers = []

    self.get = None  # type -> Operation
    self.delete = None  # type -> Operation
    self.head = None  # type -> Operation
    self.options = None  # type -> Operation
    self.patch = None  # type -> Operation
    self.post = None  # type -> Operation
    self.put = None  # type -> Operation
    self.trace = None  # type -> Operation

  def add_operation(self, operation):
    """
    Adds an operation
    Args:
      operation (swagger.paths.Operation): operation to add
    """
    http_method = operation.http_method.value.lower()
    setattr(self, http_method, operation)

  def append_path_item(self, path_item):
    pass

  def as_dict(self):
    d = swagger.core.SwaggerDict()
    if self.ref:
      d["$ref"] = self.ref
    d["summary"] = self.summary
    d["description"] = self.description

    d["get"] = self.get.as_dict() if self.get else None
    d["put"] = self.put.as_dict() if self.put else None
    d["post"] = self.post.as_dict() if self.post else None
    d["delete"] = self.delete.as_dict() if self.delete else None
    d["options"] = self.options.as_dict() if self.options else None
    d["head"] = self.head.as_dict() if self.head else None
    d["patch"] = self.patch.as_dict() if self.patch else None
    d["trace"] = self.trace.as_dict() if self.trace else None

    d["servers"] = []
    d["parameters"] = []

    d.update(super(PathItem, self).as_dict())
    return d
