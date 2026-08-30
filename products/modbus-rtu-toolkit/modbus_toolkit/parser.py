from __future__ import annotations

import re
from typing import Any

from .crc import crc16_modbus, verify_crc

FUNCTION_NAMES = {
    0x01: "Read Coils",
    0x02: "Read Discrete Inputs",
    0x03: "Read Holding Registers",
    0x04: "Read Input Registers",
    0x05: "Write Single Coil",
    0x06: "Write Single Register",
    0x0F: "Write Multiple Coils",
    0x10: "Write Multiple Registers",
}

EXCEPTION_NAMES = {
    0x01: "Illegal Function",
    0x02: "Illegal Data Address",
    0x03: "Illegal Data Value",
    0x04: "Slave Device Failure",
    0x05: "Acknowledge",
    0x06: "Slave Device Busy",
    0x08: "Memory Parity Error",
    0x0A: "Gateway Path Unavailable",
    0x0B: "Gateway Target Device Failed to Respond",
}


def parse_hex(value: str) -> bytes:
    """Parse common human-entered hex formats into bytes."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("hex input is empty")
    cleaned = value.strip().replace("0x", "").replace("0X", "")
    cleaned = re.sub(r"[\s,:;\-_]", "", cleaned)
    if not cleaned:
        raise ValueError("hex input is empty")
    if len(cleaned) % 2:
        raise ValueError("hex input must contain an even number of digits")
    if not re.fullmatch(r"[0-9a-fA-F]+", cleaned):
        raise ValueError("hex input contains non-hexadecimal characters")
    return bytes.fromhex(cleaned)


def _u16(data: bytes, index: int) -> int:
    return (data[index] << 8) | data[index + 1]


def _base(frame: bytes) -> dict[str, Any]:
    if len(frame) < 4:
        raise ValueError("Modbus RTU frame must contain address, function and two CRC bytes")
    function_raw = frame[1]
    function = function_raw & 0x7F
    received_crc = frame[-2] | (frame[-1] << 8)
    calculated_crc = crc16_modbus(frame[:-2])
    return {
        "raw_hex": frame.hex(" ").upper(),
        "length": len(frame),
        "address": frame[0],
        "function_code": function,
        "function_name": FUNCTION_NAMES.get(function, "Unknown / vendor-specific"),
        "is_exception": bool(function_raw & 0x80),
        "crc": {
            "valid": verify_crc(frame),
            "received": f"0x{received_crc:04X}",
            "calculated": f"0x{calculated_crc:04X}",
            "wire_order": f"{frame[-2]:02X} {frame[-1]:02X}",
        },
        "payload_hex": frame[2:-2].hex(" ").upper(),
        "interpretation": {},
        "warnings": [],
    }


def parse_frame(frame: bytes) -> dict[str, Any]:
    result = _base(frame)
    function_raw = frame[1]
    function = function_raw & 0x7F
    payload = frame[2:-2]

    if result["is_exception"]:
        if len(payload) != 1:
            result["warnings"].append(
                "Exception frame normally contains exactly one exception code byte"
            )
        if payload:
            code = payload[0]
            result["interpretation"] = {
                "frame_type": "exception_response",
                "exception_code": code,
                "exception_name": EXCEPTION_NAMES.get(code, "Unknown exception"),
            }
        return result

    if function in {0x03, 0x04}:
        if len(frame) == 8:
            result["interpretation"] = {
                "frame_type": "request",
                "start_address": _u16(frame, 2),
                "quantity": _u16(frame, 4),
            }
        elif payload:
            byte_count = payload[0]
            data = payload[1:]
            registers = []
            if byte_count == len(data) and byte_count % 2 == 0:
                registers = [_u16(data, i) for i in range(0, len(data), 2)]
            else:
                result["warnings"].append(
                    "Byte count does not match an even-length register payload"
                )
            result["interpretation"] = {
                "frame_type": "response",
                "byte_count": byte_count,
                "registers": registers,
            }
        else:
            result["warnings"].append("Missing function payload")

    elif function == 0x06:
        if len(frame) != 8:
            result["warnings"].append("FC06 request/response is normally 8 bytes")
        if len(payload) >= 4:
            result["interpretation"] = {
                "frame_type": "request_or_echo_response",
                "register_address": _u16(payload, 0),
                "value": _u16(payload, 2),
            }

    elif function == 0x10:
        if len(frame) == 8:
            result["interpretation"] = {
                "frame_type": "response",
                "start_address": _u16(frame, 2),
                "quantity": _u16(frame, 4),
            }
        elif len(payload) >= 5:
            start = _u16(payload, 0)
            quantity = _u16(payload, 2)
            byte_count = payload[4]
            data = payload[5:]
            registers = []
            if len(data) == byte_count and byte_count % 2 == 0:
                registers = [_u16(data, i) for i in range(0, len(data), 2)]
            else:
                result["warnings"].append("FC16 byte count does not match register data")
            if quantity * 2 != byte_count:
                result["warnings"].append("FC16 quantity and byte count are inconsistent")
            result["interpretation"] = {
                "frame_type": "request",
                "start_address": start,
                "quantity": quantity,
                "byte_count": byte_count,
                "registers": registers,
            }
        else:
            result["warnings"].append("FC16 payload is too short")

    else:
        result["interpretation"] = {
            "frame_type": "unknown",
            "note": "Function is not semantically decoded in this Alpha; raw payload is preserved.",
        }

    if not result["crc"]["valid"]:
        result["warnings"].append(
            "CRC mismatch: verify frame boundaries, byte order and copied bytes"
        )
    if not 1 <= result["address"] <= 247 and result["address"] != 0:
        result["warnings"].append(
            "Address is outside the usual Modbus slave range 1..247 (0 is broadcast)"
        )
    return result
