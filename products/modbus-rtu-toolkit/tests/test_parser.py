import unittest

from modbus_toolkit.crc import append_crc
from modbus_toolkit.parser import parse_frame, parse_hex


class TestParser(unittest.TestCase):
    def test_hex_formats(self):
        expected = bytes.fromhex("01 03 00 00 00 0A C5 CD")
        for value in [
            "01 03 00 00 00 0A C5 CD",
            "01030000000AC5CD",
            "0x01,0x03,0x00,0x00,0x00,0x0A,0xC5,0xCD",
            "01:03:00:00:00:0A:C5:CD",
        ]:
            self.assertEqual(parse_hex(value), expected)

    def test_invalid_hex(self):
        for value in ["", "123", "01 ZZ"]:
            with self.assertRaises(ValueError):
                parse_hex(value)

    def test_fc03_request(self):
        result = parse_frame(bytes.fromhex("01 03 00 00 00 0A C5 CD"))
        self.assertTrue(result["crc"]["valid"])
        self.assertEqual(result["interpretation"]["frame_type"], "request")
        self.assertEqual(result["interpretation"]["quantity"], 10)

    def test_fc03_response(self):
        frame = append_crc(bytes.fromhex("01 03 04 00 0A 00 14"))
        result = parse_frame(frame)
        self.assertEqual(result["interpretation"]["registers"], [10, 20])

    def test_exception(self):
        frame = append_crc(bytes.fromhex("01 83 02"))
        result = parse_frame(frame)
        self.assertTrue(result["is_exception"])
        self.assertEqual(result["interpretation"]["exception_name"], "Illegal Data Address")

    def test_fc06(self):
        frame = append_crc(bytes.fromhex("11 06 00 01 00 03"))
        result = parse_frame(frame)
        self.assertEqual(result["interpretation"]["register_address"], 1)
        self.assertEqual(result["interpretation"]["value"], 3)

    def test_fc16_request(self):
        frame = append_crc(bytes.fromhex("01 10 00 10 00 02 04 00 0A 00 14"))
        result = parse_frame(frame)
        self.assertEqual(result["interpretation"]["registers"], [10, 20])
        self.assertEqual(result["interpretation"]["quantity"], 2)

    def test_unknown_function_preserves_payload(self):
        frame = append_crc(bytes.fromhex("01 41 12 34"))
        result = parse_frame(frame)
        self.assertEqual(result["interpretation"]["frame_type"], "unknown")
        self.assertEqual(result["payload_hex"], "12 34")

    def test_short_frame(self):
        with self.assertRaises(ValueError):
            parse_frame(b"\x01\x03\x00")


if __name__ == "__main__":
    unittest.main()
