import unittest

from modbus_toolkit.crc import append_crc, crc16_modbus, verify_crc


class TestCrc(unittest.TestCase):
    def test_standard_read_request(self):
        body = bytes.fromhex("01 03 00 00 00 0A")
        self.assertEqual(crc16_modbus(body), 0xCDC5)
        self.assertEqual(append_crc(body), bytes.fromhex("01 03 00 00 00 0A C5 CD"))

    def test_verify(self):
        self.assertTrue(verify_crc(bytes.fromhex("01 03 00 00 00 0A C5 CD")))
        self.assertFalse(verify_crc(bytes.fromhex("01 03 00 00 00 0A C5 CE")))

    def test_short_frame(self):
        self.assertFalse(verify_crc(b"\x01\x03"))


if __name__ == "__main__":
    unittest.main()
