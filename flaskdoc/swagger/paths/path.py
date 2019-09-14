import collections

from flaskdoc.swagger import SwaggerBase


class Path(SwaggerBase):

  def __init__(self):
    super(Path, self).__init__()
    self._items = collections.OrderedDict()

  def add_path_item(self, name, path_item):
    self._items[name] = path_item

  def as_dict(self):
    d = super(Path, self).as_dict()
    d.update(self._items)


class PathItem(SwaggerBase):

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
      operation (Operation): operation to add
    Returns:

    """
    if operation.op_type == "GET":
      self.get = operation

  def append_path_item(self, path_item):
    pass

  def as_dict(self):
      d = super(PathItem, self).as_dict()
      if self.ref:
        d["$ref"] = self.ref
      d.update(collections.OrderedDict(
          summary=self.summary,
          description=self.description,
          get=self.get.as_dict()
      ))


class Operation(SwaggerBase):

  def __init__(self, responses="200", tags=None, summary=None,
               description=None, operations_id=None, parameters=None):
    super(Operation, self).__init__()
    self.responses = responses
    self.tags = tags or []
    self.summary = summary
    self.description = description
    self.operation_id = operations_id

    self.deprecated = False
    self.parameter = parameters or []
    self.op_type = None

  @staticmethod
  def from_op(op_type):
    if op_type == "GET":
      return GET()
    return None


class GET(Operation):

  def __init__(self, responses="200", tags=None, summary=None,
               description=None, operations_id=None):
    super(GET, self).__init__(responses, tags,
                              summary, description, operations_id)
    self.op_type = "GET"
