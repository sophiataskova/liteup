from liteup.lib.ppm import read_image
from liteup.schemes.base_schemes import GeneratorScheme


class ImageScan(GeneratorScheme):
    PAUSE_BETWEEN_PAINTS = 0.04

    """
    Combination of Flux and Perlin. implemented as a Perlin with the outputs
    multiplied by the flux color

    """

    def generator(self):
        offset = 0

        if self.options.center:
            offset = int(self.options.center - (self.options.num_leds / 2))

        while True:
            image_lines = read_image(self.options.from_ppm, self.options)

            led_buffer_length = self.options.num_leds * 4

            for led_line in image_lines:

                if len(led_line) < led_buffer_length:
                    self.pad_line(led_line)
                self.strip.leds = led_line[:led_buffer_length]
                self.strip.rotate(offset)
                yield True
