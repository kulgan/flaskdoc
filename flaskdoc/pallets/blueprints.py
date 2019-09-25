import flask

import mixin
from flaskdoc import swagger


class Blueprint(flask.Blueprint, mixin.SwaggerMixin):

    def __init__(self, name, import_name, static_folder=None,
                 static_url_path=None, template_folder=None,
                 url_prefix=None, subdomain=None, url_defaults=None):
        super(Blueprint, self).__init__(name, import_name, static_folder=static_folder,
                                        static_url_path=static_url_path, template_folder=template_folder,
                                        url_prefix=url_prefix, subdomain=subdomain, url_defaults=url_defaults)
        self._paths = swagger.Paths()

    def route(self, rule, ref=None, description=None, summary=None, **options):
        """ Extends flask blueprint route """
        path_item = swagger.PathItem(ref=ref, description=description, summary=summary)
        methods = options.pop("methods", ["GET"])
        operations, methods = self.extract_operations(methods)
        for operation in operations:
            path_item.add_operation(operation=operation)

        self.add_path(rule, path_item)
        options.update({"methods": methods})

        def decorator(f):

            endpoint = options.pop("endpoint", f.__name__)
            self.add_url_rule(rule, endpoint, f, **options)
            return f

        return decorator
