from setuptools import find_packages
from setuptools import setup

version = "0.0.1"
reaadme = ""

setup(
    name="FlaskDoc",
    version=version,
    author="Rowland Ogwara",
    author_email="r.ogwara@gmail.com",
    keywords="swagger, openapi, flask, rest, api",
    description="",
    classifiers=[
        "Development Status ::: Alpha Stage",
        "Topics ::: OpenAPI, flask, REST, documentation",
        "Programming Language :: Python :: 2.7"
    ],
    longdescription="",
    packages=find_packages("flaskdoc"),
    package_dir={"": "flaskdoc"},
    install_requires=[
        "six"
    ]
)
