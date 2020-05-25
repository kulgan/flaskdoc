from dataclasses import dataclass

from flaskdoc import swagger


@dataclass
class String(swagger.Schema):
    type: str = "string"


@dataclass
class Email(String):

    type: str = "string"
    format: str = "email"


@dataclass
class Int32(swagger.Schema):

    type: str = "integer"
    format: str = "int32"
    minimum: int = 0


@dataclass
class Int64(Int32):

    format: str = "int64"
