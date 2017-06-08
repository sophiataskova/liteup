#!/etc/python3
from APA102 import APA102
from easy_schemes import LuminosityTest, MaxWhite, FullScan, RandomColorChaos, RandomColorGen

NUM_LED = 390


def main():
    strip = APA102(num_led=NUM_LED,
                   order="RBG")  # Initialize the strip
    RandomColorGen(strip).start()


if __name__ == '__main__':
    main()
