import swagger.core


class Info(swagger.core.SwaggerBase):

  def __init__(self, title, version, description=None, terms_of_service=None,
               contact=None, license=None):
    """
    API metadata object
    Args:
        title (str): the title of the application (required)
        version (str): API version (required)
        description (str): short description of the application
        terms_of_service (str): API terms of service
        contact (flaskdoc.swagger.info.Contact): API contact information
        license (flaskdoc.swagger.info.License): API license information
    """
    super(Info, self).__init__()

    self.title = title
    self.description = description
    self.terms_of_service = terms_of_service
    self.contact = contact
    self.license = license
    self.version = version

  def as_dict(self):
    d = swagger.core.SwaggerDict()
    d["title"] = self.title
    d["description"] = self.description
    d["termsOfService"] = self.terms_of_service
    if self.contact:
      d["contact"] = self.contact.as_dict()
    if self.license:
      d["license"] = self.license.as_dict()
    d["version"] = self.version
    d.update(super(Info, self).as_dict())
    return d

  def __eq__(self, other):
    if not isinstance(other, Info):
      return False
    return self.title == other.title and self.version == other.version and \
           self.description == other.description and self.terms_of_service == other.terms_of_service and \
           self.contact == other.contact and self.license == other.license

  def __hash__(self):
    return hash((self.title, self.version, self.description, self.terms_of_service,
                 self.contact, self.license, self._extensions))
