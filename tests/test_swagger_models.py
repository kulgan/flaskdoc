from flaskdoc import swagger

info_block = swagger.Info(
    title="Test",
    version="1.2.2",
    terms_of_service="AAAAAAAAAA",
    contact=swagger.Contact(name="nuke", email="nuke@gmail.com", url="https://github.com/kulgan"),
    license=swagger.License(name="Apache 2.0", url="https://www.example.com/license"),
)


def test_sample_swagger():
    paths = swagger.Paths()
    item = swagger.PathItem(
        summary="Nonsense Path",
        get=swagger.GET(
            summary="Sample GET request",
            description="Test",
            tags=["sample", "rest"],
            parameters=[
                swagger.QueryParameter(name="search", required=True, description="Search Param")
            ],
            responses={},
        ),
    )

    paths.add("/echo", item)
    api = swagger.OpenApi(info_block, paths)

    swagger_json = api.to_dict()
    assert swagger_json
