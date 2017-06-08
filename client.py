from APA102 import APA102
from easy_schemes import LuminosityTest

NUM_LED = 300


def main():
    strip = APA102(num_led=NUM_LED,
                   order="RBG")  # Initialize the strip
    LuminosityTest(strip).start()


if __name__ == '__main__':
    main()
