from APA102 import APA102
from easy_schemes import MaxWhite

NUM_LED = 300


def main():
    strip = APA102(num_led=NUM_LED,
                   order="RBG")  # Initialize the strip
    MaxWhite(strip).start()


if __name__ == '__main__':
    main()
