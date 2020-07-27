from typing import List, Set

from tests.jo import models


class SoakedBean(object):

    density: int = None
    samples: List[models.Sample] = []
    squeezes: Set[models.Squeezed] = {}
