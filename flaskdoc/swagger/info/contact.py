from flaskdoc.swagger.core import SwaggerBase


class Contact(SwaggerBase):
    """ Contact information for the exposed API. """

    def __init__(self, name=None, url=None, email=None):
        super(Contact, self).__init__()

        self.email = email
        self.name = name
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, Contact):
            return False
        return self.name == other.name and self.url == other.url and self.email == other.email and \
               self._extensions == other._extensions

    def __hash__(self):
        return hash((self.url, self.email, self.name, self._extensions))
