from swagger.models import BaseModel


class OpenApi(BaseModel):
    """ This is the root document object of the OpenAPI document. """

    def __init__(self, info, paths, open_api_version="3.0.2"):
        """
        OpenApi specs tree, contains the overall specs for the API
        Args:
            open_api_version (str): Open API version used by API
            info (flaskdoc.swagger.info.Info): open api info object
            paths (flaskdoc.swagger.path.Paths): Paths definitions
        """
        super(OpenApi, self).__init__()

        self.openapi = open_api_version
        self.info = info

        # TODO disallow duplicates
        self.tags = []  # type -> swagger.tag.Tag
        self.paths = paths  # type -> swagger.path.Paths
        self.servers = set()

        self.components = None
        self.security = []

        self.external_docs = None

    def add_tag(self, tag):
        """
        Adds a tag to the top level spec
        Args:
            tag (swagger.Tag): tag to add
        """
        self.tags.append(tag)

    def add_server(self, server):
        self.servers.add(server)

    def add_paths(self, paths, url_prefix=None, blp_prefix=None):
        """
        Updates paths to include all paths in `paths`
        Args:
            paths:
            url_prefix (str): prefix
            blp_prefix (str): blueprint url prefix
        Returns:

        """
        url_prefix = url_prefix or ""
        blp_prefix = blp_prefix or ""
        for r_url in paths:
            path_url = "{}{}{}".format(url_prefix, blp_prefix, r_url)
            self.paths.add(path_url, paths.path_item(r_url))