from setuptools import find_packages
from setuptools import setup

version = "0.0.1"
reaadme = ""

setup(
    name="FlaskDoc",
    version=version,
    author="Rowland Ogwara",
    author_email="r.ogwara@gmail.com",
    description="",
    classifiers=[],
    longdescription="",
    packages=find_packages("flaskdoc"),
    package_dir={"": "flaskdoc"}
)