import flask

from blueprints import Blueprint
from flaskdoc import swagger
from mixin import SwaggerMixin


class Flask(flask.Flask, SwaggerMixin):

    def __init__(self, import_name, version, static_url_path=None, static_folder="static",
                 template_folder="templates", instance_path=None, instance_relative_config=False,
                 open_api_version="3.0.2", api_title=None):
        super(Flask, self).__init__(import_name, static_url_path=static_url_path, static_folder=static_folder,
                                    template_folder=template_folder, instance_path=instance_path,
                                    instance_relative_config=instance_relative_config)

        self.open_api = None
        self.open_api_version = open_api_version
        self.api_title = api_title
        self.api_version = version

    def swagger_init(self):
        # only initialize once
        if self.open_api:
            return

        info_block = swagger.Info(title=self.api_title, version=self.api_version)
        if self.config["API_LICENSE_NAME"]:
            license_block = swagger.License(name=self.config["API_LICENSE_NAME"],
                                            url=self.config.get("API_LICENSE_URL"))
            info_block.license = license_block
        if self.config["API_CONTACT_NAME"]:
            contact_block = swagger.Contact(name=self.config["API_CONTACT_NAME"]). \
                email(self.config.get("API_CONTACT_EMAIL")).url(self.config.get("API_CONTACT_URL"))
            info_block.contact = contact_block
        self.open_api = swagger.OpenApi(open_api_version=self.open_api_version, info=info_block, servers=None)

    def register_path(self):
        pass

    def route(self, rule, **options):

        self.swagger_init()

        super(Flask, self).route(rule, **options)

    def register_blueprint(self, blueprint, **options):

        self.swagger_init()

        if isinstance(blueprint, Blueprint):
            # custom swaggered blueprint
            pass
        super(Flask, self).register_blueprint(blueprint, **options)
