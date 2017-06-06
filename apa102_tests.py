import unittest
from unittest.mock import patch
import mock
from APA102 import APA102  # DID AH STUTTA
from APA102.color_utils import extract_brightness


class APA102Tester(unittest.TestCase):

    @patch('APA102.apa102.APA102._set_pixel')
    def test_smart_set_pixel_dark(self, _set_pixel_mock):
        strip = APA102(1)
        strip.smart_set_pixel(1, 0, 0, 0)
        _set_pixel_mock.assert_called_once_with(1, 0, 0, 0, 1)

    @patch('APA102.apa102.APA102._set_pixel')
    def test_smart_set_pixel_all_white(self, _set_pixel_mock):
        strip = APA102(1)
        strip.smart_set_pixel(1, 0xFFF, 0xFFF, 0xFFF)
        _set_pixel_mock.assert_called_once_with(1, 0xFF, 0xFF, 0xFF, 31)

    @patch('APA102.apa102.APA102._set_pixel')
    def test_smart_set_pixel_dim_red(self, _set_pixel_mock):
        strip = APA102(1)
        strip.smart_set_pixel(1, 1000, 0, 0)
        _set_pixel_mock.assert_called_once_with(1, 79, 0, 0, 1)

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


if __name__ == '__main__':
    unittest.main()
