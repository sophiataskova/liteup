#!/etc/python3
from APA102 import APA102
from all_schemes import Scheme
import configargparse
from image_strip import ImageStrip

SCHEME_CHOICES = {cls.__name__.lower(): cls for cls in Scheme.__subclasses__()}

for name, cls in SCHEME_CHOICES.items():
    print(name, cls)


parser = configargparse.ArgParser(default_config_files=['config.py', ])
parser.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
parser.add('scheme', type=str, nargs="?", help='Choose a Scheme to show!', choices=SCHEME_CHOICES, default="flux")
parser.add('-b', '--brightness', type=int, help='percentage brighness 1-100', default=100)
parser.add('--corners', type=int, action='append', help='Where meaningful start points', default=[])
parser.add('--force_hour', type=int, help='force an hour (for flux)')
parser.add('--image', type=bool, default=False, help='force an hour (for flux)')


options = parser.parse_args()
print(options)


NUM_LEDS = 390


#TODO configurable scheme!


def main():
    Stripcls = ImageStrip if options.image else APA102

    strip = Stripcls(num_leds=NUM_LEDS,
                     order="RGB",
                     max_speed_hz=1000000)  # Initialize the strip
    SchemeCls = SCHEME_CHOICES[options.scheme.lower()]

    SchemeCls(strip, options=options).start()


if __name__ == '__main__':
    main()
