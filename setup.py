from setuptools import find_packages
from setuptools import setup

version = "0.0.1a0"

setup(
    name="flaskdoc",
    version=version,
    author="Rowland Ogwara",
    author_email="r.ogwara@gmail.com",
    keywords="swagger, openapi, flask, rest, api",
    description="",
    long_description="README",
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    url="https://github.com/kulgan/flaskdoc",
    python_requires=">=3.6",
    longdescription="",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
