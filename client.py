#!/etc/python3
from APA102 import APA102
from easy_schemes import LuminosityTest, MaxWhite, FullScan, Flux
from random_schemes import Perlin
from rts import RealTimeScheme

NUM_LEDS = 390


def main():
    strip = APA102(num_leds=NUM_LEDS,
                   order="RBG",
                   max_speed_hz=6000000)  # Initialize the strip
    Flux(strip).start()


if __name__ == '__main__':
    main()
