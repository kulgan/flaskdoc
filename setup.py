from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst")) as f:
    long_description = f.read()

setup(
    name="flaskdoc",
    author="Rowland Ogwara",
    maintainer="Rowland Ogwara",
    author_email="r.ogwara@gmail.com",
    use_scm_version={"local_scheme": "dirty-tag", "version_scheme": "release-branch-semver"},
    keywords="swagger, openapi, flask, rest, api, swagger-ui",
    description="Flask wrapper for programmatically composing openapi specifications",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="Apache 2.0",
    url="https://github.com/kulgan/flaskdoc",
    python_requires=">=3.6",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    zip_safe=True,
    package_data={
        "flaskdoc": [
            "static/*.css",
            "static/*.css.map",
            "static/*.png",
            "static/*.js",
            "static/*.js.map",
            "templates/*.html",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Documentation",
    ],
    install_requires=["attrs>=19.3", "click>=7.1", "flask>=0.10", "PyYaml>=5.1"],
    extras_require={
        "dev": [
            "black",
            "click",
            "coverage[toml]",
            "flake8",
            "openapi-spec-validator",
            "pre-commit",
            "pytest",
            "pytest-cov",
            "pytest-flask",
            "sphinx",
            "sphinx_rtd_theme",
            "sphinxcontrib-napoleon",
        ],
        "rtd": ["sphinx", "sphinxcontrib-napoleon"],
    },
    setup_requires=["setuptools_scm"],
    project_urls={"source": "https://github.com/kulgan/flaskdoc"},
    entry_points={"console_scripts": ["flaskdoc = flaskdoc.cli:flaskdoc"]},
)
