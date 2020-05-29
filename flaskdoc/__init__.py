""" Developer friendly tool for crafting OpenAPI specs

    Provides OpenAPI models, decorators and swagger ui
"""
from flaskdoc.pallets import Blueprint, Flask, register_openapi
from flaskdoc.schema import Email, Int32, Int64, String

__version__ = "0.0.1a1"

