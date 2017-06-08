#!/etc/python3
from APA102 import APA102
from easy_schemes import LuminosityTest, MaxWhite, FullScan
from random_schemes import Perlin

NUM_LED = 390


def main():
    strip = APA102(num_led=NUM_LED,
                   order="RBG")  # Initialize the strip
    Perlin(strip).start()


if __name__ == '__main__':
    main()
