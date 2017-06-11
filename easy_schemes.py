from scheme import Scheme
from APA102.color_utils import gamma_correct_color
from random import randint
from base_schemes import GeneratorScheme
from datetime import datetime
import time


class Strobe(Scheme):
    HERTZ = 10

    def paint(self):
        self.setall((0xFF, 0xFF, 0xFF, 50))
        self.strip.show()
        time.sleep(1 / self.HERTZ)
        self.strip.clear_strip()


class MaxWhite(Scheme):
    PAUSE_BETWEEN_PAINTS = 0.6

    def init(self):
        self.setall((0xFF, 0xFF, 0xFF, 100))

    def paint(self):
        return False


class Flux(Scheme):
    PAUSE_BETWEEN_PAINTS = 0.0

    time_window_colors = [
        (0, 1, [0xF0, 0x90, 0x01, 1]),
        (1, 2, [0xC0, 0x50, 0x00, 1]),
        (2, 8, [0x00, 0x00, 0x00, 0]),
        # bright enough during the day
        (10, 18, [0x00, 0x00, 0x00, 0]),
        (18, 21, [0xFF, 0xFF, 0xFF, 100]),
        (21, 23, [0xFF, 0xEF, 0xAF, 100]),
        (23, 0, [0xF0, 0x0A, 0x01, 1]),
    ]

    def init(self):
        self.transitions = []
        self.cur_color = self.get_fluxed_color()
        self.setall(self.cur_color)
        return self.paint()

    def paint(self):
        # we do 10 minute transitions between flux colors!
        # if self.transitions:
        #     for trans in self.transitions:
        #         try:
        #             next(trans)
        #         except StopIteration:
        #             self.transitions.remove(trans)
        #     return True

        new_color = self.get_fluxed_color()
        if new_color != self.cur_color:
            for led in range(self.strip.num_leds):

                # trans = self.fade(led, self.cur_color, new_color, steps=100)
                # self.transitions.append(trans)
                pass

        self.setall(new_color)
        return True

        self.cur_color = new_color

    def get_fluxed_color(self, force_hour=22):

        cur_hour = datetime.now().hour
        cur_hour = force_hour

        color = [0x00, 0x00, 0x00, 0]

        for window_start, _, window_color in self.time_window_colors:
            if force_hour < window_start:
                break

            color = gamma_correct_color(window_color)
        print("going to color %s from %s to %s %s", color, window_start, _,)
        return color


class FullScan(Scheme):
    PAUSE_BETWEEN_PAINTS = 0.1
    color = [0, 0, 0]
    color_step = [1, 0, 0]

    def init(self):
        self.setall(self.color)

    def paint(self):
        self.color = [val + step for val, step in zip(self.color, self.color_step)]

        if max(self.color) > 0xFF:
            self.color = [0, 0, 0]
            self.color_step.append(self.color_step.pop(0))

        self.setall(self.color + [31])
        return True


class LuminosityTest(Scheme):
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
