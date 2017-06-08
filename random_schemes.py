from scheme import Scheme
from base_schemes import GeneratorScheme, InterpolateScheme
from lib.perlin import gen_perlin_ints


class RandomColorChaos(Scheme):
    PAUSE_BETWEEN_PAINTS = 1.5

    def paint(self):
        for led in range(self.strip.num_led):
            self.strip.set_pixel(led, randint(0, 256), randint(0, 256), randint(0, 256), 1)
        return True


class RandomColorGen(GeneratorScheme):
    PAUSE_BETWEEN_PAINTS = 1.5

    def generator(self):
        while True:
            for led in range(self.strip.num_led):
                self.strip.set_pixel(led, randint(0, 256), randint(0, 256), randint(0, 256), 1)
                yield True


class Perlin(GeneratorScheme, InterpolateScheme):
    PAUSE_BETWEEN_PAINTS = 0.04

    def generator(self):
        sub_gens = []

        r_perlin = gen_perlin_ints(0, 255)
        g_perlin = gen_perlin_ints(0, 255)
        b_perlin = gen_perlin_ints(0, 255)
        brightness_perlin = gen_perlin_ints(0, 100)
        while True:
            for led in range(self.strip.num_led):
                cur_color = self.strip.get_pixel(led)
                new_color = [next(r_perlin),
                             next(g_perlin),
                             next(b_perlin),
                             next(brightness_perlin)]

                sub_gens.append(self.paint_lin_interp(led, cur_color, new_color, steps=100))

                for sub_gen in sub_gens:
                    # we have a tail of colors we want to update
                    try:
                        next(sub_gen)
                    except StopIteration:
                        sub_gens.remove(sub_gen)

                yield True
