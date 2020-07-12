from typing import List, Set

from tests.schema import models


class SoakedBean(object):

    density: int = None
    samples: List[models.Sample] = []
    squeezes: Set[models.Squeezed] = {}
