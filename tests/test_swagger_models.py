from __future__ import print_function

from flaskdoc import swagger


def test_sample_swagger():
    # metadata info
    _info = swagger.Info(title="Test",
                         version="1.2.2",
                         contact=swagger.Contact(name="Rowland"),
                         license=swagger.License(name="Apache 2.0"))

    paths = swagger.Paths()
    item = swagger.PathItem(summary="Nonsense Path",
                            get=swagger.GET(summary="Sample GET request",
                                            description="Test",
                                            tags=["sample", "rest"],
                                            parameters=[
                                                swagger.QueryParameter(name="search", required=True,
                                                                       description="Search Param")
                                            ]))

    paths.add_path_item("/echo", item)
    api = swagger.OpenApi(_info, paths)

    swagger_json = api.as_dict()
    print(api)
    assert swagger_json
