import enum

from flaskdoc import jo, swagger


@jo.schema(camel_case_props=True)
class Item:
    api_key = jo.string(description="To be used as a dataset parameter value")
    api_version_number = jo.string(description="To be used as a version parameter value")
    api_url = jo.string(
        str_format="urlref", description="The URL describing the dataset's fields"
    )
    api_documentation_url = jo.string(
        str_format="urlref", description="A URL to the API console for each API"
    )
    api_status = jo.string()
    field_count = jo.integer()
    fields = jo.array(item=swagger.String())
    last_data_updated_date = jo.string()


@jo.schema()
class DataSetList:
    total = jo.integer()
    apis = jo.array(item=Item)


sample = DataSetList(
    total=2,
    apis=[
        Item(
            api_key="oa_citations",
            api_version_number="v1",
            api_url="https://developer.uspto.gov/ds-api/oa_citations/v1/fields",
            api_documentation_url="https://developer.uspto.gov/ds-api-docs/index.html?url=https://developer.uspto.gov"
            "/ds-api/swagger/docs/oa_citations.json",
        ),
        Item(
            api_key="cancer_moonshot",
            api_version_number="v1",
            api_url="https://developer.uspto.gov/ds-api/cancer_moonshot/v1/fields",
            api_documentation_url="https://developer.uspto.gov/ds-api-docs/index.html?url=https://developer.uspto.gov"
            "/ds-api/swagger/docs/cancer_moonshot.json",
        ),
    ],
)

list_available = swagger.GET(
    tags=["metadata"],
    summary="List available data sets",
    operation_id="list-data-sets",
    responses={
        "200": swagger.ResponseObject(
            description="Returns a list of data sets",
            content=swagger.JsonType(schema=DataSetList, example=sample),
        )
    },
)


get_info = swagger.GET(
    tags=["metadata"],
    summary="Provides the general information about the API and the list of fields that can be used to query the "
    "dataset.",
    description="This GET API returns the list of all the searchable field names that are in the oa_citations. Please "
    "see the 'fields' attribute which returns an array of field names. Each field or a combination of "
    "fields can be searched using the syntax options shown below. ",
    operation_id="list-searchable-fields",
    parameters=[
        swagger.PathParameter(
            name="dataset",
            description="Name of the dataset.",
            example="oa_citations",
            schema=swagger.String(),
        ),
        swagger.PathParameter(
            name="version",
            description="Version of the dataset.",
            example="v1",
            schema=swagger.String(),
        ),
    ],
    responses={
        "200": swagger.ResponseObject(
            description="The dataset API for the given version is found and it is accessible to consume.",
            content=swagger.JsonType(Item),
        ),
        "404": swagger.ResponseObject(
            description="The combination of dataset name and version is not found in the system or it is not "
            "published yet toc be consumed by public.",
            content=swagger.JsonType(Item),
        ),
    },
)
