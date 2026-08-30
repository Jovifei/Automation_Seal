# Product specification

## User problem

Engineers frequently receive Modbus RTU frames but spend time manually checking CRC, byte order, function codes, register addresses, quantities and exception responses.

## Alpha outcome

Given one RTU frame, the tool returns a structured explanation and CRC status in under one second on a normal desktop.

## Supported Alpha functions

- Generic frame metadata;
- FC03 Read Holding Registers;
- FC04 Read Input Registers;
- FC06 Write Single Register;
- FC16 Write Multiple Registers;
- Exception frames;
- CRC calculation and verification.

## Acceptance criteria

- Known CRC vectors pass;
- malformed hex input raises a clear error;
- short frames are rejected;
- request and response shapes are distinguished conservatively;
- unknown function codes still return raw payload without guessing;
- output contains no external calls or telemetry;
- package can be built from a clean copy using Python 3.11+.
