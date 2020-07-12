import six

from flaskdoc import swagger


class SwaggerMixin(object):
    def __init__(self):
        # collection of path items, param is here as a placeholder
        # child classes will have their own version of this variable
        self._paths = swagger.Paths()

    def add_path(self, relative_path, path_item):
        """
        Adds a path_item to existing list
        Args:
          relative_path (str): path
          path_item (swagger.PathItem):
        """
        relative_path = self.extract_path(relative_path)
        recorded_path_item = self._paths.get(relative_path)
        if recorded_path_item:
            recorded_path_item.merge(path_item)
        else:
            self._paths.add(relative_path, path_item)

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
            return [swagger.Tag(name=tags)]
        tags = [swagger.Tag(name=t) if isinstance(t, six.string_types) else t for t in tags]
        return tags

    @staticmethod
    def extract_operations(methods, responses):
        """
        Extracts operations
        Args:
          methods (swagger.Operation|list[str|swagger.Operation])): operations

        Returns:
          tuple list[swagger.Operations], list[str]: swagger operations and flask methods
        """
        if isinstance(methods, swagger.Operation):
            return [methods], [methods.http_method.value]
        methods = [
            swagger.Operation.from_op(m, responses) if isinstance(m, six.string_types) else m
            for m in methods
        ]
        flask_methods = [m.http_method.value for m in methods]
        return methods, flask_methods

    @property
    def paths(self):
        return self._paths

    def parse_route(
        self,
        rule,
        ref=None,
        description=None,
        summary=None,
        servers=None,
        parameters=None,
        responses=None,
        **options
    ):
        path_item = swagger.PathItem(
            ref=ref,
            description=description,
            summary=summary,
            servers=servers,
            parameters=parameters,
        )
        methods = options.pop("methods", ["GET"])
        operations, methods = self.extract_operations(methods, responses)
        for operation in operations:
            path_item.add_operation(operation=operation)

        self.add_path(rule, path_item)
        options.update({"methods": methods})
        return options
