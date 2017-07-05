from liteup.schemes.easy_schemes import LuminosityTest, MaxWhite, FullScan, Flux, Strobe
from liteup.schemes.random_schemes import RandomColorFade, RandomColorChaos, Perlin
from liteup.schemes.muni import Muni
from liteup.schemes.scheme import Scheme
from liteup.schemes.base_schemes import GeneratorScheme
from liteup.schemes.perflux import PerFlux
from liteup.schemes.rts import RTS
from liteup.schemes.imagescan import ImageScan
from liteup.schemes.twinkle_scheme import TwinkleScheme

Scheme_subclasses = Scheme.__subclasses__()
all_schemes = Scheme.__subclasses__()
# get all schemes anywhere underneath Scheme.
# There are subclasses at least 2 lvls deep
for scheme in all_schemes:
    all_schemes.extend(scheme.__subclasses__())

all_schemes = list(set(all_schemes))

SCHEME_CHOICES = {cls.__name__.lower(): cls for cls in all_schemes}
