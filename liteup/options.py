import configargparse

from liteup.schemes.all_schemes import all_schemes, SCHEME_CHOICES


for name, cls in SCHEME_CHOICES.items():
    print(name, cls)

parser = configargparse.ArgParser(default_config_files=['config.py', ])
parser.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
parser.add('scheme', type=str, nargs="?", help='Choose a Scheme to show!', choices=SCHEME_CHOICES, default="flux")
parser.add('-b', '--brightness', type=int, help='percentage brighness 1-100', default=100)
parser.add('--corners', type=int, action='append', help='Where are meaningful start points in the installation?', default=[])
parser.add('--force_hour', type=int, help='force an hour (for flux)')
parser.add('--save_image', type=bool, default=False, help='Output an image file (image.ppm) instead of writing to leds')
parser.add('--num_leds', type=int, default=390, help='how many leds to light up')
parser.add('--from_ppm', type=str, help='ImageScan scheme can scan over a ppm image')

# for a in parser._actions:
# print(repr(a))
# MWahahaha


def parse_options():
    options = parser.parse_args()
    return options
