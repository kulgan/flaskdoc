import collections
import six

from flaskdoc.swagger import Operation, Tag


class SwaggerMixin(object):

    def __init__(self):
        # collection of path items, param is here as a placeholder
        # child classes will have their own version of this variable
        self.api_paths = collections.OrderedDict()  # type -> dict[str, path.PathItem]

    def add_path(self, relative_path, path_item):
        """
        Adds a path_item to existing list
        Args:
          relative_path (str): path
          path_item (swagger.PathItem):
        """
        relative_path = self.extract_path(relative_path)
        item = self.api_paths.get(relative_path)
        if not item:
            self.api_paths[relative_path] = path_item
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
          list[swagger.Tag]: list of tags
        """
        if isinstance(tags, six.string_types):
            return [Tag(name=tags)]
        tags = [Tag(name=t) if isinstance(t, six.string_types) else t for t in tags]
        return tags

    @staticmethod
    def extract_operations(methods):
        """
        Extracts operations
        Args:
          methods (swagger.Operation|list[str|swagger.Operation])): operations

        Returns:
          tuple list[swagger.Operations], list[str]: swagger operations and flask methods
        """
        if isinstance(methods, Operation):
            return [methods], [methods.http_method]
        methods = [Operation.from_op(m) if isinstance(m, six.string_types) else m for m in
                   methods]
        flask_methods = [m.http_method for m in methods]
        return methods, flask_methods
