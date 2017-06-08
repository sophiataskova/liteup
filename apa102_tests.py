import unittest
from unittest.mock import patch
import mock
from APA102 import APA102  # DID AH STUTTA
from APA102.color_utils import extract_brightness


class APA102Tester(unittest.TestCase):

    @patch('APA102.apa102.APA102._set_pixel')
    def test_smart_set_pixel_dark(self, _set_pixel_mock):
        strip = APA102(1)
        strip.smart_set_pixel(0, 0, 0, 0)
        _set_pixel_mock.assert_called_once_with(0, 0, 0, 0, 1)

    @patch('APA102.apa102.APA102._set_pixel')
    def test_smart_set_pixel_all_white(self, _set_pixel_mock):
        strip = APA102(1)
        strip.smart_set_pixel(0, 0xFFF, 0xFFF, 0xFFF)
        _set_pixel_mock.assert_called_once_with(0, 0xFF, 0xFF, 0xFF, 31)

    @unittest.skip("smartpixel disabled")
    @patch('APA102.apa102.APA102._set_pixel')
    def test_smart_set_pixel_dim_red(self, _set_pixel_mock):
        strip = APA102(1)
        strip.smart_set_pixel(0, 1000, 0, 0)
        _set_pixel_mock.assert_called_once_with(0, 79, 0, 0, 1)

    def test_extract_brightness(self):
        # 1 0000 0000
        #   1000 0000  10
        shifted_tup = extract_brightness(1 << 7, 0, 0)
        self.assertEqual(shifted_tup, (1 << 7, 0, 0, 1))

    def test_extract_brightness(self):
        # 1 0000 0000
        #   1000 0000  11
        shifted_tup = extract_brightness(1 << 8, 0, 0)
        self.assertEqual(shifted_tup, (1 << 7, 0, 0, 3))

    def test_extract_brightness_bright(self):
        # 1000 0000 0000
        #      1000 0000  1111
        shifted_tup = extract_brightness(1 << 11, 0, 0)
        self.assertEqual(shifted_tup, (1 << 7, 0, 0, 31))

    def test_hidden_set_then_hidden_get(self):
        strip = APA102(1)
        strip._set_pixel(0, 0xFF, 0xFF, 0xFF, 10)
        self.assertEqual(strip._get_pixel(0), [0xFF, 0xFF, 0xFF, 10])

    def test_set_then_get(self):
        strip = APA102(1)
        strip._set_pixel(0, 0xFF, 0xFF, 0xFF, 10)
        # There's some inaccuracy due to our rounding to convert percentage
        # to brightness int
        self.assertEqual(strip.get_pixel(0), [0xFF, 0xFF, 0xFF, 32])


if __name__ == '__main__':
    unittest.main()
