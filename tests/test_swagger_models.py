from flaskdoc import swagger


def test_sample_swagger(info_block):
    paths = swagger.Paths()
    item = swagger.PathItem(summary="Nonsense Path",
                            get=swagger.GET(summary="Sample GET request",
                                            description="Test",
                                            tags=["sample", "rest"],
                                            parameters=[
                                                swagger.QueryParameter(name="search", required=True,
                                                                       description="Search Param")
                                            ], responses=swagger.ResponsesObject()))

    paths.add("/echo", item)
    api = swagger.OpenApi(info_block, paths)

    swagger_json = api.dict()
    assert swagger_json
