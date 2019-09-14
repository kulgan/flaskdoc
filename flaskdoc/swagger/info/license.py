from flaskdoc.swagger.base import SwaggerBase


class License(SwaggerBase):

    def __init__(self, name, url=None):
        super(License, self).__init__()
        self.url = url
        self.name = name

    def as_dict(self):
        st = super(License, self).as_dict()
        st.update(dict(
            url=self.url,
            name=self.name
        ))

        return st

    def __eq__(self, other):
        if not isinstance(other, License):
            return False
        return self.name == other.name and self.url == other.url and \
               self._extensions == other._extensions

    def __hash__(self):
        return hash((self.url, self.name, self._extensions))
