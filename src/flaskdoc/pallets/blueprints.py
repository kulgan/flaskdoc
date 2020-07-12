import flask

from flaskdoc import swagger
from flaskdoc.pallets import mixin


class Blueprint(flask.Blueprint, mixin.SwaggerMixin):
    def __init__(
        self,
        name,
        import_name,
        static_folder=None,
        static_url_path=None,
        template_folder=None,
        url_prefix=None,
        subdomain=None,
        url_defaults=None,
    ):
        super(Blueprint, self).__init__(
            name,
            import_name,
            static_folder=static_folder,
            static_url_path=static_url_path,
            template_folder=template_folder,
            url_prefix=url_prefix,
            subdomain=subdomain,
            url_defaults=url_defaults,
        )
        self._paths = swagger.Paths()

    def route(
        self,
        rule,
        ref=None,
        description=None,
        summary=None,
        servers=None,
        parameters=None,
        responses=None,
        **options
    ):
        """
        Extends flask blueprint route
        Args:
            rule (str): rule name
            ref (str): Allows for an external definition of this path item.
            description (str): An optional, string description, intended to apply to all operations in this path.
            summary (str): An optional, string summary, intended to apply to all operations in this path.
            servers (List[swagger.Server]): server list
            parameters (List[swagger.Parameter]): list of parameters
            responses (swagger.ResponsesObject):
            **options:

        Returns:
            callback:
        """

        options = self.parse_route(
            rule, ref, description, summary, servers, parameters, responses, **options
        )
        return super(Blueprint, self).route(rule, **options)
