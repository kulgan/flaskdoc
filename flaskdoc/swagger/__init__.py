from base import SwaggerBase


class OpenApi(SwaggerBase):

    def __init__(self, open_api_version, info, servers):
        """

        Args:
            open_api_version (str): Open API version used by API
            info (flaskdoc.swagger.info.Info): open api info object
        """
        super(OpenApi, self).__init__()

        self.open_api = open_api_version
        self.info = info
