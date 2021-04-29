from enum import Enum

import attr

from flaskdoc import jo


@attr.s
class SoapStar(object):
    """Simple attr based class"""

    meal = attr.ib(type=float)
    smokes = attr.ib(default=10)


@attr.s
class Sample(object):
    """Class with mixed attribute definitions"""

    danni = "fear"
    palo = attr.ib(type=int)
    soap = attr.ib(type=SoapStar)
    hulu = attr.ib(default="NoNo")


class OakTown:
    """Sample class without any special annotations"""

    oaks = None
    smugs = 1  # type: int
    snux = "2"  # type: str
    # sample = Sample(palo=1, soap=SoapStar(meal=1.2))


class Squeezed:
    """Sample class with typed annotations"""

    sample = 1
    spaces = 6

    def hangout(self):
        return self.sample


class Color(Enum):
    black = "black"
    white = "white"
    pint = "pinksys"


@jo.schema()
class Lemons(object):
    name = jo.string(str_format="uuid", required=True, enum=[None, "a", "b"])
    size = jo.integer(maximum=1000)
    flows = jo.one_of(types=[Squeezed, OakTown])
    samples = jo.array(item=Sample, required=True, min_items=1)
    star = jo.object(SoapStar, required=True)
    color = jo.object(Color, required=True)


if __name__ == "__main__":
    print(Lemons.jo_schema().json())
