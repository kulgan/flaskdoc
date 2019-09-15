from __future__ import print_function

from swagger import OpenApi
from swagger import info, paths, tag

if __name__ == '__main__':
  _info = info.Info(title="Test", version="1.2.2")
  contact = info.Contact(name="Rowland")
  license = info.License(name="Apache 2.0")
  license.add_extension("x-axis", 234)
  _info.contact = contact
  _info.license = license

  path = paths.Paths()
  item = paths.PathItem(summary="Nonsense Path")
  op = paths.GET()
  item.add_operation(op)

  path.add_path_item("/echo", item)
  api = OpenApi("3.0.2", _info, None)
  api.paths = path
  api.add_tag(tag.Tag(name="test", description="test tag"))
  print(api)
