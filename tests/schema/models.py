from typing import List

import attr


@attr.s
class SoapStar(object):
    """ Simple attr based class """

    meal = attr.ib(type=float)
    smokes = attr.ib(default=10)


@attr.s
class Sample(object):
    """ Class with mixed attribute definitions """

    danni = "fear"
    palo = attr.ib(type=int)
    soap = attr.ib(type=SoapStar)
    hulu = attr.ib(default="NoNo")


class OakTown:
    """ Sample class without any special annotations """

    oaks = None
    smugs = 0  # type: int
    snux = "2"  # type: str


class Squeezed:
    """ Sample class with typed annotations """

    sample = 1
    spaces = 6

    def hangout(self):
        return self.sample


# py36 and higher typing annotations
class SoakedBean(object):

    density: int = None
    samples: List[Sample] = []
