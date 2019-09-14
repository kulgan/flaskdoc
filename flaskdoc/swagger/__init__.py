from base import SwaggerBase


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
    self.paths = []  # type -> swagger.paths.Path

  def add_tag(self, tag):
    """
    Adds a tag to the top level spec
    Args:
        tag (swagger.tag.Tag): tag to add
    """
    self.tags.append(tag)

  def add_path(self, path):
    """
    Adds a new path
    Args:
        path (swagger.paths.Path): path to add
    """
    self.paths.append(path)

  def as_dict(self):
    d = super(OpenApi, self).as_dict()
    d.update(dict(
      openapi=self.open_api,
      info=self.info.as_dict(),
      paths=[path.as_dict() for path in self.paths],
      tags=[tag.as_dict() for tag in self.tags]
    ))

    return d
