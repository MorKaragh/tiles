from gaming_grid import GridSquare, GamingGrid
from functools import partial 


def testfun(a, b, c):
    print(f"{a} {b} {c}")


part = partial(testfun, a=1, b=3, c=2)

part()
