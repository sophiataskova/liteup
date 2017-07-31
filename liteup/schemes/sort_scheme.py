import colorsys
from random import random
from liteup.lib.color import Color
from liteup.schemes.base_schemes import GeneratorScheme
# merge sort!


def clean_array():
    array = []
    for _ in range(390):
        raw_color = colorsys.hsv_to_rgb(random(), 1.0, 1.0)
        new_color = Color(*(255 * v for v in raw_color),
                          brightness=1, gamma=True)
        array.append(new_color)
    return array


def quicksort(array, start, stop):
    if stop - start < 2:
        return True

    larger_index = stop - 2
    smaller_index = start
    # the "whole" starts where the pivot does
    pivot = array[stop - 1]
    hole = stop - 1

    while larger_index + 1 > smaller_index:
        if pivot < array[larger_index]:
            print('larger')
            # good case, this is the right side
            # just shift the whole and continue!
            array[hole] = array[larger_index]
            larger_index -= 1
            hole -= 1
            yield [hole]
        else:
            print('smaller')
            # gotta put it on the other side
            tmp = array[larger_index]
            array[larger_index] = array[smaller_index]

            array[smaller_index] = tmp
            smaller_index += 1
            yield [smaller_index, larger_index]

    array[hole] = pivot
    yield [hole]

    yield from quicksort(array, start, hole)
    yield from quicksort(array, hole + 1, stop)


class Sort(GeneratorScheme):
    PAUSE_BETWEEN_PAINTS = 0.00001   # Override to control animation speed!

    def generator(self):
        array = clean_array()

        for highlight in quicksort(array, 0, self.options.num_leds):
            yield self.draw(array, highlight)

        while True:
            import time
            yield self.draw(array, [])
            time.sleep(1)
            yield self.draw(sorted(array), [])
            time.sleep(1)

    def draw(self, array, highlights):
        for idx, color in enumerate(array):
            # TODO highlight modifications
            if idx in highlights:
                color.paint(self.strip, idx, brightness=100)
            else:
                color.paint(self.strip, idx)

        return True
