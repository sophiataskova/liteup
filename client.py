#!/etc/python3
from APA102 import APA102
from image_strip import ImageStrip

from options.py import otions, SCHEME_CHOICES


#TODO configurable scheme!


def main():
    Stripcls = ImageStrip if options.save_image else APA102

    strip = Stripcls(num_leds=options.num_leds,
                     order="RGB",
                     max_speed_hz=1000000)  # Initialize the strip
    SchemeCls = SCHEME_CHOICES[options.scheme.lower()]

    SchemeCls(strip, options=options).start()


if __name__ == '__main__':
    main()
