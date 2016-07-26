import serial
from struct import pack, unpack

# May need to pad, given the 2-byte words in MSP430.
# sync bytes: 0xA0, 0xFF, 0x00, 0xAA
#  these happen at the beginning.
# They're NOT included in this format:
# '<' = little-endian
# '>' = big-endian
mating_format = '<BBBBHQH'

#ser = serial.Serial('/dev/ttyUSB0')
#serial_message = []

#mate_payload_tuple = struct.unpack(mating_format, serial_message)

# (
    # proto_version,
    # from_addr,
    # hat_award_id,
    # camo_id,
    # flags,
    # achievements,
    # crc16
# ) = mate_payload_tuple

# print mate_payload_tuple

with serial.Serial('/dev/ttyS1', 9600) as ser:
    while True:
        print '%02x' % ser.read()