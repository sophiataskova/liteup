from scheme import Scheme
from APA102.color_utils import extract_brightness
from random import randint
from base_schemes import Solid, GeneratorScheme, InterpolateScheme
from datetime import datetime


def log_wire(r, g, b):
    # r = gamma_correct(r)
    # b = gamma_correct(b)
    # g = gamma_correct(g)

    print(extract_brightness(r, g, b))


class MaxWhite(Solid):
    PAUSE_BETWEEN_PAINTS = 60

    def init(self):
        self.setall((0xFFF, 0xFFF, 0xFFF))

    def paint(self):
        return False


class Flux(Solid, InterpolateScheme):
    PAUSE_BETWEEN_PAINTS = 60

    time_window_colors = [
        (0, 1, [0x30, 0x0A, 0x01, 1]),
        (1, 2, [0x03, 0x01, 0x03, 1]),
        (2, 8, [0x00, 0x00, 0x00, 0]),
        # bright enough during the day
        (10, 18, [0x00, 0x00, 0x00, 0]),
        (18, 21, [0xFF, 0xFF, 0xFF, 100]),
        (21, 23, [0xA0, 0x20, 0x10, 1]),
        (23, 0, [0x30, 0x0A, 0x01, 1]),
    ]

    def init(self):
        self.transitions = []
        self.cur_color = self.get_fluxed_color()
        self.setall(self.cur_color)
        return self.paint()

    def paint(self):
        # we do 10 minute transitions between flux colors!
        if self.transitions:
            for trans in self.transitions:
                try:
                    next(trans)
                except StopIteration:
                    self.transitions.remove(trans)
            return True

        new_color = self.get_fluxed_color()
        if new_color != self.cur_color:
            for led in range(self.strip.num_leds):
                trans = self.paint_lin_interp(led, self.cur_color, new_color)
                self.transitions.append(trans)

        self.cur_color = new_color

    def get_fluxed_color(self):
        cur_hour = datetime.now().hour
        color = [0x00, 0x00, 0x00, 0]

        for window_start, _, window_color in self.time_window_colors:
            if cur_hour < window_start:
                break
            color = window_color
        return color


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

        self.setall(self.color + [31])
        return True


class LuminosityTest(Solid):
    PAUSE_BETWEEN_PAINTS = 600

    def init(self):
        dim = 50
        bright = 255
        for led in range(0, self.strip.num_leds, 3):
            self.strip.set_pixel(led, dim, 0, 0, bright_percent=100)
            self.strip.set_pixel(led + 1, dim, dim, dim, bright_percent=100)
            self.strip.set_pixel(led + 2, bright, bright, bright, bright_percent=3)

    def paint(self):
        return False
