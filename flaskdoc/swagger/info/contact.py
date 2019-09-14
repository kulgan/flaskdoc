from flaskdoc.swagger.base import SwaggerBase


class Contact(SwaggerBase):

    def __init__(self, name=None, url=None, email=None):
        super(Contact, self).__init__()

        self.email = email
        self.name = name
        self.url = url

    def as_dict(self):
        st = super(Contact, self).as_dict()
        st.update(dict(
            url=self.url,
            name=self.name,
            email=self.email
        ))

        return st

    def __eq__(self, other):
        if not isinstance(other, Contact):
            return False
        return self.name == other.name and self.url == other.url and \
               self.email == other.email and self._extensions == other._extensions

    def __hash__(self):
        return hash((self.url, self.email, self.name, self._extensions))

