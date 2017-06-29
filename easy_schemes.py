from scheme import Scheme
from APA102.color_utils import gamma_correct_color
from random import randint
from base_schemes import GeneratorScheme
from datetime import datetime, timedelta
import itertools
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
        self.setall((0xFF, 0xFF, 0xFF, self.options.brightness))

    def paint(self):
        return False


class Nice(Scheme):
    PAUSE_BETWEEN_PAINTS = 100000

    def init(self):
        self.setall([0xFF, 0x45, 0x05, 40])

    def paint(self):
        return False


class Dark(Scheme):
    PAUSE_BETWEEN_PAINTS = 100000

    def init(self):
        self.setall([0x00, 0x00, 0x00, 0])

    def paint(self):
        return False


class Flux(Scheme):
    PAUSE_BETWEEN_PAINTS = 1.0
    autofade = True

    time_window_colors = [
        (0, 1, [0x19, 0x02, 0x00, 1]),
        (1, 8, [0x00, 0x00, 0x00, 0]),
        # sunrise!
        (8, 10, [0xFF, 0xFF, 0xFF, 100]),
        # Green - go to work
        (10, 11, [0x00, 0xFF, 0x00, 100]),
        # bright enough during the day
        (11, 18, [0x00, 0x00, 0x00, 0]),
        (18, 20, [0xFF, 0xFF, 0xFF, 100]),
        (20, 22, [0xFF, 0x45, 0x05, 40]),
        (22, 23, [0x90, 0x25, 0x00, 30]),
        (23, 0, [0x90, 0x19, 0x0, 10]),
    ]

    def init(self):
        self.cur_color = self.get_fluxed_color()
        self.setall(self.cur_color)
        self.strip.show()

    def paint(self):
        new_color = gamma_correct_color(self.get_fluxed_color())
        if new_color != self.cur_color:
            print("twinkly transitioning to %s" % new_color)
            for led in range(self.strip.num_leds):
                # we want a twinkly transition
                wait = self.wait(randint(0, 5 * 60))
                fade = self.fade(led, self.cur_color, new_color, steps=60)
                trans = itertools.chain(wait, fade)
                self.transitions.append(trans)

        self.cur_color = new_color

    def get_fluxed_color(self):

        cur_hour = datetime.now().hour
        if self.options.force_hour is not None:
            cur_hour = self.options.force_hour

        color = [0x00, 0x00, 0x00, 0]

        for window_start, _, window_color in self.time_window_colors:
            if cur_hour < window_start:
                break

            color = window_color
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
