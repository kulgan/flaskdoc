from __future__ import print_function

from flaskdoc import swagger

if __name__ == '__main__':
  _info = swagger.Info(title="Test", version="1.2.2")
  contact = swagger.Contact(name="Rowland")
  license = swagger.License(name="Apache 2.0")
  license.add_extension("x-axis", 234)
  _info.contact = contact
  _info.license = license

  path = swagger.Paths()
  item = swagger.PathItem(summary="Nonsense Path")
  op = swagger.GET(summary="Sample GET request", description="Test", tags=["sample", "rest"])
  p = swagger.Parameter(name="search", location="query", required=True, description="Search Param")
  op.add_parameter(p)
  item.add_operation(op)

  path.add_path_item("/echo", item)
  api = swagger.OpenApi("3.0.2", _info, None)
  api.paths = path
  api.add_tag(swagger.Tag(name="test", description="test tag"))
  print(api)
