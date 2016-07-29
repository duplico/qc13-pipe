import crcmod
import serial
from struct import pack, unpack

# May need to pad, given the 2-byte words in MSP430.
# sync bytes: 0xA0, 0xFF, 0x00, 0xAA
#  these happen at the beginning.
# They're NOT included in this format:
# '<' = little-endian
# '>' = big-endian
mating_format = '<BBBBHQH'
mating_format_nocrc = '<BBBBHQ'


# print mate_payload_tuple

sync_bytes = [0xA0, 0xFF, 0x00, 0xAA]
sync_position = 0
payload_len = 16
payload = ''

crc_check = crcmod.mkCrcFun(0b10001000000100001, rev=False)

def handle_input(payload):
    (proto_version,
     from_addr,
     hat_award_id,
     camo_id,
     flags,
     achievements,
     crc16) = payload
    c = crc_check(pack(mating_format_nocrc, proto_version, from_addr, hat_award_id, camo_id, flags, achievements))
    print mate_payload_tuple
    print 'id %d with hat %d' % (from_addr, hat_award_id)


with serial.Serial('/dev/ttyUSB0', 9600) as ser:
    while True:
        in_byte = ser.read()
        if sync_position < 4:
            if ord(in_byte) == sync_bytes[sync_position]:
                sync_position += 1
            else:
                sync_position = 0
                payload = ''
        elif len(payload) == payload_len-1:
            payload += in_byte
            sync_position = 0
            mate_payload_tuple = unpack(mating_format, payload)
            handle_input(mate_payload_tuple)
            payload = ''
        else:
            payload += in_byte
