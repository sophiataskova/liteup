"""The module contains the base Scheme class"""

import time
import sys


class Scheme:
    """
    This is the base for all Scheme objects.
    They are similar to the color cycle template provided by APA102, but Schemes
    are intended to display perpetually (without the notion of *cycles*), and there
    is a larger client that controls starting and stopping Schemes.
    TODO: Schemes are also able to recieve configurable arguments from the API

    Schemes are intended to keep track of their own state, such as where they are
    in their animation. It should be incremented during each *update* call

    A specific scheme must subclass this template, and implement at least the
    'paint' method.
    """

    PAUSE_BETWEEN_PAINTS = 0.001  # Override to control animation speed!

    def __init__(self, strip, options):
        self.strip = strip
        self.options = options

    def init(self):
        """This method is called to initialize a Scheme.

        #TODO configurable arguments!

        The default does nothing. A particular subclass could setup
        variables, or even light the strip in an initial color.
        """
        pass

    def shutdown(self):
        """This method is called before exiting.

        The default does nothing
        """
        pass

    def paint(self):
        """
        This method paints one subcycle. It must be implemented.
        """

        raise NotImplementedError("Please implement the paint() method")

    def cleanup(self):
        """Cleanup method."""
        self.shutdown()
        self.strip.clear_strip()
        self.strip.cleanup()

    def start(self):
        """This method does the actual work."""
        try:
            print("Starting: %s" % self.__class__.__name__)
            self.strip.clear_strip()
            self.init()  # Call the subclasses init method
            self.strip.show()
            while True:  # Loop forever
                need_repaint = self.paint()
                if need_repaint:
                    self.strip.show()  # repaint if required
                # TODO asyncio yield-sleep?
                time.sleep(self.PAUSE_BETWEEN_PAINTS)  # Pause until the next step

        finally:
            # Finished, cleanup everything
            self.cleanup()

    # A bunch of utility functions!
    def setall(self, color):
        for led in range(self.strip.num_leds):
            self.strip.set_pixel(led, *color)

    def tick_generators(self, gen_list):
        for gen in gen_list:
            try:
                next(gen)
            except StopIteration:
                gen_list.remove(gen)

    def fade(self, led_num, start_color, target_color, steps=10):
        """
        Returns a generator that will paint this pixel to the target over some
        steps. good with tick_generators()

        This uses linear interpretation.
        maybe another kind of interpretation would also be cool?

        """

        for cur_step in range(steps):
            stepcolor = [
                self.lin_interp(cur_step, steps, start_val, target_val)
                for start_val, target_val in zip(start_color, target_color)
            ]
            self.strip.set_pixel(led_num, *stepcolor)
            yield True

    @staticmethod
    def lin_interp(cur_step, num_steps, start_val, target_val):

        return int(start_val + ((target_val - start_val) * (cur_step / num_steps)))
