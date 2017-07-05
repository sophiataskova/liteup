
from easy_schemes import LuminosityTest, MaxWhite, FullScan, Flux, Strobe
from random_schemes import RandomColorFade, RandomColorChaos, Perlin
from muni import Muni
from scheme import Scheme
from base_schemes import GeneratorScheme
from perflux import PerFlux
from rts import RTS
from imagescan import ImageScan
from twinkle_scheme import TwinkleScheme

all_schemes = Scheme.__subclasses__() + GeneratorScheme.__subclasses__()

SCHEME_CHOICES = {cls.__name__.lower(): cls for cls in all_schemes}
