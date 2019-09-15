from flaskdoc.swagger import base


class Paths(base.SwaggerBase):

  def __init__(self, path_items=None):
    super(Paths, self).__init__()
    self._items = path_items

  def add_path_item(self, name, path_item):
    if not self._items:
      self._items = base.SwaggerDict()
    self._items[name] = path_item

  def as_dict(self):
    d = base.SwaggerDict()
    for k, v in self._items.items():
      d[k] = v.as_dict()
    d.update(super(Paths, self).as_dict())
    return d


class PathItem(base.SwaggerBase):

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
    d = base.SwaggerDict()
    if self.ref:
      d["$ref"] = self.ref
    d["summary"] = self.summary
    d["description"] = self.description
    if self.get:
      d["get"] = self.get.as_dict()
    d.update(super(PathItem, self).as_dict())
    return d


class Operation(base.SwaggerBase):

  def __init__(self, responses="200", tags=None, summary=None,
               description=None, operations_id=None, parameters=None):
    super(Operation, self).__init__()
    self.responses = responses
    self.tags = tags or []
    self.summary = summary
    self.description = description
    self.operation_id = operations_id

    self.deprecated = False
    self.parameters = parameters or []
    self.op_type = None

  def add_parameter(self, parameter):
    self.parameters.append(parameter)

  @staticmethod
  def from_op(op_type):
    if op_type == "GET":
      return GET()
    return None

  def as_dict(self):
    d = base.SwaggerDict()
    d["tags"] = [t.as_dict() for t in self.tags]
    d["summary"] = self.summary
    d["description"] = self.description


class GET(Operation):

  def __init__(self, responses="200", tags=None, summary=None,
               description=None, operations_id=None):
    super(GET, self).__init__(responses, tags,
                              summary, description, operations_id)
    self.op_type = "GET"
