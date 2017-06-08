# TODO do I like this?
GAMMA_CORRECT_FACTOR = 2.8


def extract_brightness(r, g, b):
    # These are 12 bits, but we want to shift them to 8
    # we'll use the shift distance to set the brightness val
    # this effectively gives us more value at the bottom
    ## Bitlength is 1- indexed.  1.bit_length() == 1, but it's in the 0th place

    max_bit_length = max(r, g, b).bit_length()

    shift_dist = 0
    if max_bit_length > 8:
        shift_dist = (max_bit_length - 8)

    brightness = (1 << (shift_dist + 1)) - 1

    if shift_dist:
        r = r >> shift_dist
        g = g >> shift_dist
        b = b >> shift_dist

    return (r, g, b, brightness)


def gamma_correct(led_val, num_bits):
    max_val = (1 << num_bits) - 1.0
    corrected = pow(led_val / max_val, GAMMA_CORRECT_FACTOR) * max_val
    return int(corrected)
