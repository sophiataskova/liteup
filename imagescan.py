from base_schemes import GeneratorScheme
from lib.ppm import read_image


class ImageScan(GeneratorScheme):
    """
    Combination of Flux and Perlin. implemented as a Perlin with the outputs
    multiplied by the flux color

    """

    def generator(self):
        image_lines = read_image(options.from_ppm)

        led_buffer_length = options.num_leds * 4

        for led_line in image_lines:
            if len(led_line) < led_buffer_length:
                self.pad_line(led_line)
            self.leds = self.led_line[:led_buffer_length]
            yield True
