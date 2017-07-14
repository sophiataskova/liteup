import random
from liteup.schemes.scheme import Scheme

ENERGY_FROM_FOOD = 2
MOVE_ENERGY = 0.05


class Critter:
    init_energy = 5

    def __init__(self, place, team):
        self.place = place
        self.team = team
        self.energy = self.init_energy

    def move(self):
        if self.energy < 0:
            return None

        move_options = [-1, 1] + [0] * 10
        move_choice = random.choice(move_options)
        if move_choice != 0:
            self.energy = self.energy - MOVE_ENERGY
        return move_choice

    def fight(self, other_critter, strip):
        if other_critter.team != self.team:
            print("FIGHT")
            strip.set_pixel_rgb(self.place, 0xFFFFFF, 100)
            self.energy -= 1
            other_critter.energy -= 1

    def eat(self, breed_callback):
        self.energy += ENERGY_FROM_FOOD
        print(self.energy)
        if self.energy >= 100:
            self.energy = 1
            breed_callback(self.place, self.team)

    def draw(self, strip):
        color = [0xFF00000, self.energy]
        if self.team:
            color = [0x00FF, self.energy]

        strip.set_pixel_rgb(self.place, *color)


class RTS(Scheme):
    """
    A Scheme built like a real-time strategy game!
    RTS = Real time Scheme
    """

    init_food = 200
    step_food = 1

    def init(self):
        self.generate_food(self.init_food)
        self.generate_critters()
        self.critters = []
        self.food = set()

    def paint(self):
        self.paint_background()

        self.generate_food(self.step_food)
        self.paint_food()
        self.move_critters()
        print(len(self.critters))
        return True

    def generate_critters(self):
        self.critters.append(Critter(0, False))
        opposite = int(self.strip.num_leds / 2)
        self.critters.append(Critter(opposite, True))

    def generate_food(self, numfood):
        all_places = set(range(self.strip.num_leds))

        empty_spaces = all_places - self.food

        numfood = min(numfood, len(empty_spaces))
        new_food_spaces = random.sample(empty_spaces, numfood)
        for new_food_space in new_food_spaces:
            self.food.add(new_food_space)

    def paint_background(self):
        for led in range(self.strip.num_leds):
            self.strip.set_pixel(led, 1, 1, 1, 1)

    def paint_food(self):
        for food_place in self.food:
            self.strip.set_pixel(food_place, 0, 100, 0, 1)

    def move_critters(self):
        critter_places = {critter.place: critter for critter in self.critters}
        for critter in self.critters:
            place = critter.place

            movement = critter.move()
            if movement is None:

                self.critters.remove(critter)
                del critter_places[place]
                continue

            new_place = (place + movement + self.strip.num_leds) % self.strip.num_leds
            if new_place > self.strip.num_leds:
                new_place = new_place - self.strip.num_leds

            if new_place in critter_places and critter_places[new_place] is not critter:
                # don't move there, just fight it
                critter.fight(critter_places[new_place], self.strip)
                continue

            critter.place = new_place

            if new_place in self.food:
                self.food.discard(new_place)
                critter.eat(breed_callback=self.add_child)

            critter.draw(self.strip)

    def add_child(self, place, team):
        """
        called by critter!
        """

        def _add_child(new_place):
            self.critters.append(Critter(new_place, team))

        critter_places = {critter.place: critter for critter in self.critters}
        if place - 1 not in critter_places:
            _add_child(place - 1)

        if place + 1 not in critter_places:
            _add_child(place + 1)
