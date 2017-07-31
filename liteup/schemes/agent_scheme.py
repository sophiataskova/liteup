from liteup.schemes.base_schemes import GeneratorScheme
from enum import Enum
from random import random, randint
from liteup.lib.color import Color

FOODMAX = 40


class Agent:
    def __init__(self):
        self.color = Color.make_random(self.max_hue, self.brightness)
        # TODO somehow draw from options?
        self.loc = randint(0, 390)

    def paint(self, strip):
        self.color.paint(strip, int(self.loc % 390))


class Food(Agent):
    brightness = 2
    max_hue = 40


class Spider(Agent):
    brightness = 100
    max_hue = 40

    def __init__(self, loc, color):
        super(Spider, self).__init__()
        self.loc = loc
        self.color = color
        self.speed = 0.1

    def move(self, env):
        oldloc = self.loc
        self.loc = (self.loc + self.speed) % 390
        stepped = int(self.loc) != int(oldloc)


class Crab(Agent):
    brightness = 20
    max_hue = 100
    moods = Enum("mood", "count gather")

    def __init__(self):
        super(Crab, self).__init__()
        self.speed = 0
        self.holding = None
        self.mood = self.moods.gather

    def move(self, env):
        oldloc = self.loc
        self.loc = (self.loc + self.speed) % 390
        stepped = int(self.loc) != int(oldloc)

        if random() < 0.05:
            # adjust speed only sometimes
            self.speed = (((0.5 - random()) / 3) + self.speed)
            self.speed = min(0.3, self.speed)
            self.speed = max(-0.3, self.speed)

        if self.holding:
            # I want the holding object to trail 'behind'
            direction = self.speed / abs(self.speed)
            self.holding.loc = (self.loc - direction) % 390

        on_food = env.food_at(int(self.loc))
        # If I'm already at a food, drop it and go to count
        if on_food:
            if self.holding:
                self.holding = None
                self.mood = self.moods.count
                self.count = 2

            elif self.mood == self.moods.gather:
                # I found a food! grab it and turn around
                self.holding = on_food
                self.speed = self.speed * -2

            elif self.mood == self.moods.count and stepped:
                self.count += 1
                print(self.count)
                self.speed = self.speed * 1.1
                # if we stepped, this is a new one!
                if self.count > 5:
                    self.count = 0
                    self.speed = self.speed * 4
                    env.spiders.append(Spider(self.loc, self.color))
                    print(f"MAKING SPIDER {len(env.spiders)}")
        else:
            self.mood = self.moods.gather


class Environment:

    def __init__(self):
        self.food = []
        self.crabs = []
        self.spiders = []

    def step(self):
        if len(self.food) < FOODMAX:
            self.food.append(Food())

        if len(self.crabs) < 5:
            self.crabs.append(Crab())

        for c in self.crabs:
            c.move(self)

        for s in self.spiders:
            s.move(self)

    def paint(self, strip):
        for f in self.food:
            f.paint(strip)
        for c in self.crabs:
            c.paint(strip)
        for s in self.spiders:
            s.paint(strip)

    def food_at(self, loc):
        for f in self.food:
            if int(f.loc) == loc:
                return f
        return None


class AgentScheme(GeneratorScheme):
    PAUSE_BETWEEN_PAINTS = 0.01   # Override to control animation speed!

    def generator(self):
        background = [Color.make_random(2, brightness=1) for _ in range(390)]
        environment = Environment()

        while True:
            environment.step()
            for idx, color in enumerate(background):
                color.paint(self.strip, idx)
            environment.paint(self.strip)

            yield True
