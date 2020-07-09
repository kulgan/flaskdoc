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
    smugs: int = 0
    snux = "2"


class Squeezed:
    """ Sample class with typed annotations """

    sample: int
    spaces: str

    def hangout(self):
        return self.sample
