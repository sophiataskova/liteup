from liteup.schemes.base_schemes import generatorScheme
import random

FOODMAX = 40


class Color:
    __slots__ = ["r", "g", "b", "brightness"]

    def init(r, g, bm brightness):
        self.r = r
        self.g = g
        self.b = b
        self.brightness = brightness

    @classmethod
    def make_random(cls, maxval, brightness)
        return cls(random.randint(0, maxval),
                   random.randint(0, maxval),
                   random.randint(0, maxval),
                   brightness)

    def paint(strip, number):
        strip.set_pixel(number, self.r, self.g, self.b, brightness)


class Agent:
    def __init__(self):
        self.color = Color.make_random(self.max_hue, self.brightness)
        # TODO somehow draw from options?
        self.loc = random.randint(0, 390)

    def paint(strip):
        self.color.paint(strip, self.loc)


class Food(Agent):
    brightness = 40
    max_hue = 40


class Crab(Agent):
    brightness = 80
    max_hue = 100

    def walk():
        self.loc = (self.loc + random.randint(-1, 1)) % 390


class AgentScheme(generatorScheme):

    def paint():
        background = [Color.make_random(5, brightness=1) for _ in range(390)]
        food = []
        crabs = []

        while True:
            for idx, color in enumerate(background):
                color.paint(self.strip, idx)

            if len(food) < FOODMAX:
                food.append(Food())

            for f in food:
                f.paint()

            if len(crabs) < 0:
                crabs.append(Crab())

            for c in crabs:
                c.move()
                c.paint()

            yield True
            if len(food) < FOODMAX:
