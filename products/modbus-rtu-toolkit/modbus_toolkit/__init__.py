"""Jovi Modbus RTU diagnostic toolkit."""

from .crc import append_crc, crc16_modbus, verify_crc
from .parser import parse_frame, parse_hex

__all__ = ["append_crc", "crc16_modbus", "verify_crc", "parse_frame", "parse_hex"]
__version__ = "0.1.0"
