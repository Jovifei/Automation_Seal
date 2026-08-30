from __future__ import annotations


def crc16_modbus(data: bytes) -> int:
    """Return the Modbus CRC16 integer for *data*.

    The wire representation is little-endian: low byte first, high byte second.
    """
    crc = 0xFFFF
    for value in data:
        crc ^= value
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF


def append_crc(data: bytes) -> bytes:
    crc = crc16_modbus(data)
    return data + bytes((crc & 0xFF, (crc >> 8) & 0xFF))


def verify_crc(frame: bytes) -> bool:
    if len(frame) < 4:
        return False
    expected = crc16_modbus(frame[:-2])
    received = frame[-2] | (frame[-1] << 8)
    return expected == received
