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
    classifiers=[
        "Development Status :: 2 - Alpha",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Documentation"
    ],
    longdescription="",
    packages=find_packages(exclude="tests"),
    include_package_data=True,
    install_requires=[
        "flask",
        "PyYaml"
    ],
    package_data={
        "flaskdoc": [
            "LICENSE",
            "README.md",
            "static/*.css",
            "static/*.html",
            "static/*.js",
            "static/*.png",
            "templates/*.html",
        ]
    }
)
