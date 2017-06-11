#!/etc/python3
from APA102 import APA102
from easy_schemes import LuminosityTest, MaxWhite, FullScan, Flux
from random_schemes import Perlin
from rts import RTS
import configargparse

schemes = [LuminosityTest, MaxWhite, FullScan, Flux, RTS, Perlin]
SCHEME_CHOICES = {cls.__name__.lower(): cls for cls in schemes}


parser = configargparse.ArgParser(default_config_files=['config.py', ])
parser.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
parser.add('scheme', type=str, nargs="?", help='What scheme to show!')
# , choices=SCHEME_CHOICES, default="flux")
parser.add('-b', '--brightness', type=int, help='percentage brighness 1-100', default=100)
parser.add('--corners', type=int, action='append', help='Where meaningful start points', default=[])


options = parser.parse_args()
print(options)


NUM_LEDS = 390


#TODO configurable scheme!


def main():
    strip = APA102(num_leds=NUM_LEDS,
                   order="RGB",
                   max_speed_hz=6000000)  # Initialize the strip
    SchemeCls = SCHEME_CHOICES[options.scheme.lower()]

    SchemeCls(strip, options=options).start()


if __name__ == '__main__':
    main()
