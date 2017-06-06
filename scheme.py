"""The module contains the base Scheme class"""

import time
import apa102
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

    pause_between_updates = 0.001  # Override to control animation speed!

    def __init__(self, strip):
        self.strip = strip

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
            self.strip.clear_strip()
            self.init()  # Call the subclasses init method
            self.strip.show()
            while True:  # Loop forever
                need_repaint = self.update()
                if need_repaint:
                    self.strip.show()  # repaint if required
                # TODO asyncio yield-sleep?
                time.sleep(self.pause_between_updates)  # Pause until the next step

        finally:
            # Finished, cleanup everything
            self.cleanup()
