from typing import List, Set

from flaskdoc.swagger import schema_factory
from tests.jo import models


class SoakedBean(object):

    density: int = None
    samples: List[models.Sample] = []
    squeezes: Set[models.Squeezed] = {}
