from scheme import Scheme
from APA102.color_utils import extract_brightness


def log_wire(r, g, b):
    # r = gamma_correct(r)
    # b = gamma_correct(b)
    # g = gamma_correct(g)

    print extract_brightness(r, g, b)


class Solid(Scheme):
    # abstract base
    def setall(self, color):
        log_wire(*color)
        for led in range(self.strip.num_led):
            self.strip.set_pixel(led, *color)


class MaxWhite(Solid):
    PAUSE_BETWEEN_PAINTS = 60

    def init(self):
        self.setall((0xFFF, 0xFFF, 0xFFF))

    def paint(self):
        return False


class FullScan(Solid):
    PAUSE_BETWEEN_PAINTS = 0.1
    color = [0, 0, 0]
    color_step = [1, 0, 1]

    def init(self):
        self.setall(self.color)

    def paint(self):
        self.color = [val + step for val, step in zip(self.color, self.color_step)]

        if max(self.color) > 0xFF:
            self.color = [0, 0, 0]
            self.color_step.append(self.color_step.pop(0))

        self.setall(self.color)
        return True


class LuminosityTest(Solid):
    PAUSE_BETWEEN_PAINTS = 600

    def init(self):
        dim = 50
        bright = 255
        for led in range(0, self.strip.num_led, 3):
            self.strip.set_pixel(led, dim, 0, 0, bright_percent=100)
            self.strip.set_pixel(led + 1, dim, dim, dim, bright_percent=100)
            self.strip.set_pixel(led + 2, bright, bright, bright, bright_percent=3)

    def paint(self):
        return False
