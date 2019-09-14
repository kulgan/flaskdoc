import collections
import six

from swagger import tag, paths


class SwaggerMixin(object):

  def __init__(self):
    # collection of path items, param is here as a placeholder
    # child classes will have their own version of this variable
    self.api_paths = collections.OrderedDict()  # type -> dict[str, paths.PathItem]

  def add_path(self, path, path_item):
    """
    Adds a path_item to existing list
    Args:
      path (str): path
      path_item (paths.PathItem):
    """
    path = self.extract_path(path)
    item = self.api_paths.get(path)
    if not item:
      self.api_paths[path] = path_item
    item.appen_path_item(path_item)

  @staticmethod
  def extract_path(path):
    return path

  @staticmethod
  def extract_tags(tags):
    """
    Extract tags from list
    Args:
      tags (str|list[str|tag.Tag]): tags to add

    Returns:
      list[tag.Tag]: list of tags
    """
    if isinstance(tags, six.string_types):
      return [tag.Tag(name=tags)]
    tags = [tag.Tag(name=tag) if isinstance(t, six.string_types) else t for t in tags]
    return tags

  @staticmethod
  def extract_operations(methods):
    """
    Extracts operations
    Args:
      methods (paths.Operation|list[str|path.Operation])): operations

    Returns:
      tuple list[paths.Operations], list[str]: swagger operations and flask methods
    """
    if isinstance(methods, paths.Operation):
      return [methods], [methods.op_type]
    methods = [paths.Operation.from_op(m) if isinstance(m, six.string_types) else m for m in methods]
    flask_methods = [m.op_type for m in methods]
    return methods, flask_methods
