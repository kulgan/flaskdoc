from swagger.models import SwaggerDict
from swagger import BaseModel, Style


class Content(BaseModel):

    def __init__(self):
        super(Content, self).__init__()
        self.contents = SwaggerDict()

    def add_media_type(self, name, media_type):
        self.contents[name] = media_type.dict()

    def dict(self):
        return self.contents




