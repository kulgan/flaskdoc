import flask


class Flask(flask.Flask):

    def __init__(self, import_name, static_url_path=None, static_folder="static",
                 template_folder="templates", instance_path=None, instance_relative_config=False):
        super(Flask, self).__init__(import_name, static_url_path=static_url_path, static_folder=static_folder,
                                    template_folder=template_folder, instance_path=instance_path,
                                    instance_relative_config=instance_relative_config)
        self.version = None
        self.contact = None
        self.license = None
