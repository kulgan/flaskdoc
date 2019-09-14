import flask


class Blueprint(flask.Blueprint):

    def __init__(self, name, import_name, static_folder=None,
                 static_url_path=None, template_folder=None,
                 url_prefix=None, subdomain=None, url_defaults=None):
        super(Blueprint, self).__init__(name, import_name, static_folder=static_folder,
                                        static_url_path=static_url_path, template_folder=template_folder,
                                        url_prefix=url_prefix, subdomain=subdomain, url_defaults=url_defaults)

    def route(self, rule, ref=None, description=None, tags=None, **options):
        super(Blueprint, self).route(rule, **options)
