from scheme import Scheme


class Solid(Scheme):
    def init(color):
        self.color = color

    def paint():
        for led in range(self.strip.num_leds):
            self.strip.set_pixel_rgb(self.color)
        return True
