import json
import dataclasses

from pydantic.dataclasses import dataclass
from pydantic.schema import schema


@dataclass
class Pro:

    def __init__(self):
        self.x = 1
        self.y = None


print(json.dumps(schema([Pro()])))
