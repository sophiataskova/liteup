import apa102
from easy_schemes import MaxWhite


def main():
    strip = apa102.APA102(num_led=self.num_led,
                          global_brightness=self.global_brightness,
                          order="RBG")  # Initialize the strip
    MaxWhite(strip).start()
