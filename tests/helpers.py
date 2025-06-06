import pathlib
import time
from functools import lru_cache

from pyvrp import ProblemData
from pyvrp.read import read as _read
from pyvrp.read import read_solution as _read_solution
from pyvrp.search._search import Node, Route

# Full path to the data directory used in tests.
DATA_DIR = pathlib.Path(__file__).parent / "data"


@lru_cache
def read(where: str, *args, **kwargs):
    """
    Lightweight wrapper around ``pyvrp.read.read()``, reading problem files
    relative to the current directory.
    """
    this_dir = pathlib.Path(__file__).parent
    return _read(this_dir / where, *args, **kwargs)


def read_solution(where: str, *args, **kwargs):
    """
    Lightweight wrapper around ``pyvrp.read.read_solution()``, reading solution
    files relative to the current directory.
    """
    this_dir = pathlib.Path(__file__).parent
    return _read_solution(this_dir / where, *args, **kwargs)


def sleep(duration, get_now=time.perf_counter):
    """
    Custom sleep function. Built-in ``time.sleep()`` is not precise/depends on
    the OS, see https://stackoverflow.com/q/1133857/4316405.
    """
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()


def make_search_route(
    data: ProblemData,
    visits: list[int],
    idx: int = 0,
    vehicle_type: int = 0,
):
    """
    Helper for a common test idiom: creating a ``pyvrp.search.Route``, adding
    nodes for the given visits to it, and then calling ``update()`` to populate
    the route's statistics.
    """
    route = Route(data, idx, vehicle_type)
    for visit in visits:
        route.append(Node(loc=visit))
    route.update()
    return route
