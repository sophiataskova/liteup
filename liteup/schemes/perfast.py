from liteup.lib.perlin import gen_perlin_ints
from liteup.schemes.easy_schemes import Flux
from liteup.schemes.random_schemes import Perlin


class PerFast(Perlin, Flux):
    """
    Perlin but ready for a party!
    """
    PAUSE_BETWEEN_PAINTS = 0.0

    num_steps = 2
    perlin_octaves = 2
    ui_select = True
