import collections
import six

from flaskdoc.swagger import Operation, Paths, Tag


class SwaggerMixin(object):

    def __init__(self):
        # collection of path items, param is here as a placeholder
        # child classes will have their own version of this variable
        self._paths = Paths()

    def add_path(self, relative_path, path_item):
        """
        Adds a path_item to existing list
        Args:
          relative_path (str): path
          path_item (swagger.PathItem):
        """
        relative_path = self.extract_path(relative_path)
        recorded_path_item = self._paths.path_item(relative_path)
        if recorded_path_item:
            recorded_path_item.merge(path_item)
        else:
            self._paths.add_path_item(relative_path, path_item)

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
            return [methods], [methods.http_method.value]
        methods = [Operation.from_op(m) if isinstance(m, six.string_types) else m for m in
                   methods]
        flask_methods = [m.http_method.value for m in methods]
        return methods, flask_methods

    @property
    def paths(self):
        return self._paths
