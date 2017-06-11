from scheme import Scheme
from base_schemes import GeneratorScheme, InterpolateScheme
from lib.perlin import gen_perlin_ints
from APA102.color_utils import gamma_correct
import config


class RandomColorChaos(Scheme):
    PAUSE_BETWEEN_PAINTS = 1.5

    def paint(self):
        for led in range(self.strip.num_leds):
            self.strip.set_pixel(led, randint(0, 256), randint(0, 256), randint(0, 256), 1)
        return True


class RandomColorGen(GeneratorScheme):
    PAUSE_BETWEEN_PAINTS = 1.5

    def generator(self):
        while True:
            for led in range(self.strip.num_leds):
                self.strip.set_pixel(led, randint(0, 256), randint(0, 256), randint(0, 256), 1)
                yield True


class Perlin(GeneratorScheme, InterpolateScheme):
    PAUSE_BETWEEN_PAINTS = 0.04

    # how long the perlin wave is, and how fast they adjust
    num_steps = 50
    # how chaotic the perlin is. higher is more stable
    perlin_octaves = 6

    def generator(self):
        waves = [
            self.perlin_wave(corner)
            for corner in config.corners
        ]
        while True:
            self.tick_generators(waves)
            yield True

    def perlin_wave(self, start_point):
        sub_gens = []

        r_perlin = gen_perlin_ints(0, 255, num_octaves=self.perlin_octaves)
        g_perlin = gen_perlin_ints(0, 255, num_octaves=self.perlin_octaves)
        b_perlin = gen_perlin_ints(0, 255, num_octaves=self.perlin_octaves)
        brightness_perlin = gen_perlin_ints(0, 100)
        while True:
            for led in range(start_point, self.strip.num_led):
                cur_color = self.strip.get_pixel(led)
                new_color = [gamma_correct(next(r_perlin)),
                             gamma_correct(next(g_perlin)),
                             gamma_correct(next(b_perlin)),
                             100]

                sub_gens.append(
                    self.paint_lin_interp(led, cur_color, new_color, steps=self.num_steps))

                # we have a tail of colors we want to update
                self.tick_generators(sub_gens)

                yield True
            start_point = 0
