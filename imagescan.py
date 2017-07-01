from base_schemes import GeneratorScheme


class ImageScan(GeneratorScheme):
    """
    Combination of Flux and Perlin. implemented as a Perlin with the outputs
    multiplied by the flux color

    """
    num_steps = 100

    def make_waves(self, max_colors):
        fluxr, fluxg, fluxb, brightness = max_colors
        r_perlin = gen_perlin_ints(0, fluxr, num_octaves=self.perlin_octaves)
        g_perlin = gen_perlin_ints(0, fluxg, num_octaves=self.perlin_octaves)
        b_perlin = gen_perlin_ints(0, fluxb, num_octaves=self.perlin_octaves)
        return r_perlin, g_perlin, b_perlin, brightness

    def perlin_wave(self, start_point):
        sub_gens = []
        cur_flux_color = self.get_fluxed_color()
        r_perlin, g_perlin, b_perlin, brightness = self.make_waves(cur_flux_color)
        while True:
            new_flux_color = self.get_fluxed_color()
            if new_flux_color != cur_flux_color:
                r_perlin, g_perlin, b_perlin, brightness = self.make_waves(cur_flux_color)
                cur_flux_color = new_flux_color

            for led in range(start_point, self.strip.num_leds):
                cur_color = self.strip.get_pixel(led)
                new_color = [next(r_perlin),
                             next(g_perlin),
                             next(b_perlin),
                             brightness]
                sub_gens.append(
                    self.fade(led, cur_color, new_color, steps=self.num_steps))

                # we have a tail of colors we want to update

                self.tick_generators(sub_gens)

                yield True
            start_point = 0
