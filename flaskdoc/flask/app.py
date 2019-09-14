import flask

from flaskdoc import swagger
from flaskdoc.flask import blueprints
from flaskdoc.swagger import info


class Flask(flask.Flask):

    def __init__(self, import_name, version, static_url_path=None, static_folder="static",
                 template_folder="templates", instance_path=None, instance_relative_config=False,
                 open_api_version="3.0.2", api_title=None):
        super(Flask, self).__init__(import_name, static_url_path=static_url_path, static_folder=static_folder,
                                    template_folder=template_folder, instance_path=instance_path,
                                    instance_relative_config=instance_relative_config)
        
        self.open_api = None
        self.swagger_init(open_api_version, api_title, version)
    
    def swagger_init(self, open_api_version, title, version):
        info_block = info.Info(title=title, version=version)
        if self.config["API_LICENSE_NAME"]:
            license_block = info.License(name=self.config["API_LICENSE_NAME"],
                                         url=self.config.get("API_LICENSE_URL"))
        info_block.license = license_block
        if self.config["API_CONTACT_NAME"]:
            contact_block = info.Contact(name=self.config["API_CONTACT_NAME"]). \
                email(self.config.get("API_CONTACT_EMAIL")).url(self.config.get("API_CONTACT_URL"))
            info_block.contact = contact_block
        self.open_api = swagger.OpenApi(open_api_version=open_api_version, info=info_block, servers=None)
    
    def route(self, rule, **options):
        super(Flask, self).route(rule, **options)

    def register_blueprint(self, blueprint, **options):
        if isinstance(blueprint, blueprints.Blueprint):
            # custom swaggered blueprint
            pass
        super(Flask, self).register_blueprint(blueprint, **options)
