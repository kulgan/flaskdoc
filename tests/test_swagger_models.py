import swagger.models
from flaskdoc import swagger


def test_sample_swagger(info_block):

    paths = swagger.models.Paths()
    item = swagger.models.PathItem(summary="Nonsense Path",
                                   get=swagger.models.GET(summary="Sample GET request",
                                                          description="Test",
                                                          tags=["sample", "rest"],
                                                          parameters=[
                                                swagger.models.QueryParameter(name="search", required=True,
                                                                              description="Search Param")
                                            ]))

    paths.add("/echo", item)
    api = swagger.models.OpenApi(info_block, paths)

    swagger_json = api.dict()
    assert swagger_json
