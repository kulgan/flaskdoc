import pathlib2
from setuptools import find_packages
from setuptools import setup

version = "0.0.1-alpha"

# The directory containing this file
HERE = pathlib2.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="FlaskDoc",
    version=version,
    author="Rowland Ogwara",
    author_email="r.ogwara@gmail.com",
    keywords="swagger, openapi, flask, rest, api",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    url="https://github.com/kulgan/flaskdoc",
    classifiers=[
        "Development Status :: 2 - Alpha",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Documentation"
    ],
    longdescription="",
    packages=find_packages("flaskdoc", exclude="tests"),
    include_package_data=True,
    package_dir={"": "flaskdoc"},
    install_requires=[
        "flask",
        "six",
        "PyYaml"
    ]
)
