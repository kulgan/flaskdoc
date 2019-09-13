from flaskdoc.swagger.base import SwaggerBase


class ExternalDocumentation(SwaggerBase):

    def __init__(self, url, description=None):
        
        super(ExternalDocumentation, self).__init__()
        self.url = url
        self.description = description
