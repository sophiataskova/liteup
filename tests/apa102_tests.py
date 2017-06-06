import unittest
from unittest.mock import patch
import mock
from liteup.APA102 import APA102  # DID AH STUTTA


class APA102Tester(unittest.TestCase):

    @patch('APA102.apa102.APA102._set_pixel')
    def test_smart_set_pixel_dark(self, _set_pixel_mock):
        strip = APA102(1)
        strip.smart_set_pixel(1, 0, 0, 0)
        _set_pixel_mock.assert_called_once_with(1, 0, 0, 0, 0)

if __name__ == '__main__':
    unittest.main()
