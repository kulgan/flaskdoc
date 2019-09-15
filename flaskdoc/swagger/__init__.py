from base import SwaggerBase, SwaggerDict


class OpenApi(SwaggerBase):

  def __init__(self, open_api_version, info, servers):
    """
    OpenApi specs tree, contains the overall specs for the API
    Args:
        open_api_version (str): Open API version used by API
        info (flaskdoc.swagger.info.Info): open api info object
    """
    super(OpenApi, self).__init__()

    self.open_api = open_api_version
    self.info = info

    # TODO disallow duplicates
    self.tags = []  # type -> swagger.tag.Tag
    self.paths = None  # type -> swagger.paths.Paths

  def add_tag(self, tag):
    """
    Adds a tag to the top level spec
    Args:
        tag (swagger.tag.Tag): tag to add
    """
    self.tags.append(tag)

  def as_dict(self):
    d = SwaggerDict()
    d["openapi"] = self.open_api
    d["info"] = self.info.as_dict()
    d["paths"] = self.paths.as_dict()

    if self.tags:
      d["tags"] = [tag.as_dict() for tag in self.tags]

    d.update(super(OpenApi, self).as_dict())
    return d
