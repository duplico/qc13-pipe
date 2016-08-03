

import crcmod
import serial
from struct import pack, unpack
from bitstruct import pack as bitpack
from bitstruct import unpack as bitunpack

from generator import print_journey
from qc13conf import *

achievements_awarded = [55, 56]

mating_format = '<BBBBHQBBBBBBH'
mating_format_nocrc = '<BBBBHQBBBBBB'
flag_format = 'p4u1u1u1u1u1u1u1u1u1u1u1p1'

sync_bytes = [0xA0, 0xFF, 0x00, 0xAA]

crc_check = crcmod.mkCrcFun(0b10001000000100001, rev=False)

# When we send, f_pipe must be set, and out ID must be DEDICATED_BASE_ID

def send_pipe_message(rst, hat_id):
    hid = 0xff
    hawd = 0
    hclm = 0
    if hat_id is not None:
        hid = hat_id
        hawd = 1
        hclm = 1
        
    flags_bits = Flags(f_reprint=0, f_hat_claim_from_pipe=hclm, 
                       f_pipe=1, f_handler=0, f_badge_has_claimed_hat=0, 
                       f_rst=rst, f_hat_holder=0, f_ink=0, f_nack=0, 
                       f_ack=0, f_award=hawd)
    flags_bytes = bitpack(flag_format, *flags_bits)
    flags = ord(flags_bytes[1])
    flags += (ord(flags_bytes[0]) << 8)
    
    out_payload_tuple = MatePayloadRaw(
        proto_version=0x42,
        from_addr=DEDICATED_BASE_ID,
        hat_award_id=hid,
        camo_id=0,
        flags=flags,
        achievements=0,
        seen_count=0,
        uber_seen_count=0,
        odh_seen_count=0,
        mate_count=0,
        uber_mate_count=0,
        odh_mate_count=0,
        crc16=0
    )
    
    c = crc_check(pack(mating_format_nocrc, *out_payload_tuple[:-1]))
    out_payload_tuple = out_payload_tuple._replace(crc16=c)
    out_payload = pack(mating_format, *out_payload_tuple)
    
    # TX: sync_bytes
    ser.write(map(chr, sync_bytes))
    # TX: out_payload
    ser.write(out_payload)
    print ':::::TXed message:'
    print '   Flags sent:'
    print '    rst %d' % flags_bits.f_rst
    print '    award %d' % flags_bits.f_award
    print '    hatid %d' % out_payload_tuple.hat_award_id
    

def send_pipe_claim_hat(hat_id):
    send_pipe_message(0, hat_id)

def send_pipe_nrst():
    send_pipe_message(0, None)

def parse_payload(payload):
    print ':Message RXed:::::'
    mate_payload_tuple = MatePayloadRaw._make(unpack(mating_format, payload))
    c = crc_check(pack(mating_format_nocrc, *mate_payload_tuple[:-1]))
    if c != mate_payload_tuple.crc16:
        print '    fail: bad crc'
        return False
    
    flags0 = mate_payload_tuple.flags & 0xFF
    flags1 = (mate_payload_tuple.flags & 0xFF00) >> 8
    
    in_flags = Flags._make(bitunpack(flag_format, [flags1, flags0]))

    print '   Flags received:'
    print '    rst', in_flags.f_rst
    print '    hat awarded', in_flags.f_hat_holder
    print '    hat claimed', in_flags.f_badge_has_claimed_hat
    
    badge_achievements = []
    
    for i in hats.keys():
        if (mate_payload_tuple.achievements >> i) & 1:
            badge_achievements.append(i)
    
    return MatePayload(*(mate_payload_tuple + in_flags + (badge_achievements,)))

# Never times out - listens forever to get a new message.
# TODO: Probably should change that.
def read_payload():
    sync_position = 0
    payload_len = 22
    payload = ''
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
            r = parse_payload(payload)
            payload = ''
            sync_position = 0
            if r:
                return r
            else:
                continue
        else:
            payload += in_byte
    
def read_and_handle_achievements(payload):
    result = None
    
    print 'Achievements:', ', '.join(map(lambda a: hats[a][0], 
                                     payload.achievement_list))
    
    if payload.f_hat_holder and payload.f_badge_has_claimed_hat:
        # They already have a hat, and they've actually claimed it.
        print 'They have a hat, and they have claimed it.'
    elif payload.f_hat_holder and not payload.f_badge_has_claimed_hat and payload.hat_award_id not in achievements_awarded:
        # AWARDING THE HAT!!!
        print 'Already won, time to claim', payload.hat_award_id
        send_pipe_claim_hat(payload.hat_award_id)
        result = payload.hat_award_id
    else:
        # Let's try to find an unawarded achievement that they've
        #  earned.
        for a in hats.keys():
            if a in badge_achievements and a not in achievements_awarded:
                # It's available!
                print 'We can award hat %d' % a
                send_pipe_claim_hat(a)
                result = a
                break # Don't award ALL the hats. Lol.
    # Finally, we just need to do a print.
    # Let's let the main handle that.
    return result
    
# There's 3 different things we can get from the badge:
#   1. RST: means we reply with an ~RST
#   2. NRST: means we read its achievements and print, possibly bestow.
#   3. ACK or NACK: completes the bestow handshake.
#   4. F_REPRINT: do a print again, regardless of whether we're in
#       timeout.

with serial.Serial('/dev/ttyUSB0', 9600) as ser:
    give_hat = None
    while True:
        print "Listening..."
        p = read_payload()
        if not p:
            continue
            
        if p.f_rst:
            send_pipe_nrst()
        elif p.f_ack:
            print 'Hat accepted.'
            if give_hat is None:
                pass
            else:
                # Accepted
                # Save that the hat is awarded.
                achievements_awarded.append(give_hat)
            give_hat = None
        elif p.f_nack:
            print 'Hat refused. Ungrateful little squid...'
            give_hat = None
            print_journey(p, give_hat) # Hat refused. Ungrateful jackass...
        else:
            # Got a NRST, time to read achievements.
            give_hat = read_and_handle_achievements(p)
            if give_hat is None: print_journey(p, give_hat)
