from scheme import Scheme


class MaxWhite(Scheme):
    pause_between_updates = 60

    def init():
        for led in range(self.strip.num_leds):
            self.strip.set_pixel_rgb(0xFFFFF, 100)

    def paint():
        return False
