from scheme import Scheme


class Solid(Scheme):
    # abstract base
    def setall(self, color):
        for led in range(self.strip.num_leds):
            self.strip.set_pixel(led, *color)


class GeneratorScheme(Scheme):
    def init(self):
        self.gen = self.generator()

    def paint(self):
        return next(self.gen)


class InterpolateScheme(Scheme):

    def paint_lin_interp(self, led_num, start_color, target_color, steps=10):
        for cur_step in range(steps):
            stepcolor = [
                self.lin_interp(cur_step, steps, start_val, target_val)
                for start_val, target_val in zip(start_color, target_color)
            ]
            print(stepcolor)
            self.strip.set_pixel(led_num, *stepcolor)
            yield True

    @staticmethod
    def lin_interp(cur_step, num_steps, start_val, target_val):

        return int(start_val + ((target_val - start_val) * (cur_step / num_steps)))
