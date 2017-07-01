import unittest
from unittest.mock import patch, mock_open
from ppm import write_image, read_image

PPM_EXAMPLE = b"P6 3 3 255\n" +\
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00" +\
    b"\xFF\x00\x00\x00\xFF\x00\x00\x00\xFF" +\
    b"\x01\x02\x03\x04\x05\x06\x07\x08\x09"

LED_EXAMPLE = [
    [255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, ],
    [255, 255, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, ],
    [255, 1, 2, 3, 255, 4, 5, 6, 255, 7, 8, 9, ],
]


def get_file_from_mockopen(mo):
    calls = mo().write.call_args_list
    # get first arg from all the write calls. This is the string it wrote
    write_strs = [call[0][0] for call in calls]
    return b"".join(write_strs)


class PPMTester(unittest.TestCase):

    def test_ppm_read(self):
        with patch("ppm.open", mock_open(read_data=PPM_EXAMPLE)):
            output = read_image("testfilename")
            self.assertEqual(LED_EXAMPLE, output)

    def test_ppm_write(self):
        mo = mock_open()
        with patch("ppm.open", mo):
            write_image(LED_EXAMPLE, "testfilename")
            wrotefile = get_file_from_mockopen(mo)
            self.assertEqual(PPM_EXAMPLE, wrotefile)

    def test_ppm_read_then_write(self):
        """
        Test that read and write can work together
        """

        with patch("ppm.open", mock_open(read_data=PPM_EXAMPLE)):
            read_leds = read_image("testfilename")

        mo = mock_open()
        with patch("ppm.open", mo):
            write_image(read_leds, "testfilename")
            wrotefile = get_file_from_mockopen(mo)
            self.assertEqual(PPM_EXAMPLE, wrotefile)

    def test_ppm_write_then_read(self):
        mo = mock_open()
        with patch("ppm.open", mo):
            write_image(LED_EXAMPLE, "testfilename")
            wrotefile = get_file_from_mockopen(mo)
            self.assertEqual(PPM_EXAMPLE, wrotefile)

        with patch("ppm.open", mock_open(read_data=wrotefile)):
            read_leds = read_image("testfilename")
            self.assertEqual(read_leds, LED_EXAMPLE)


if __name__ == '__main__':
    unittest.main()
