from collections import namedtuple, OrderedDict

import crcmod
import serial
from struct import pack, unpack
from bitstruct import pack as bitpack
from bitstruct import unpack as bitunpack

achievements_awarded = [55, 56]

hats_unordered = {
    0: ("DUPLiCO's special friend", "Be chosen."),
    1: ("akio's special friend", "Be chosen."),
    2: ("Tprophet's special friend", "Be chosen."),
    3: ("Zac's special friend", "Be chosen."),
    4: ("3ric's special friend", "Be chosen."),
    5: ("Shaun's special friend", "Be chosen."),
    6: ("XEDGeek's special friend", "Be chosen."),
    7: ("Jason's special friend", "Be chosen."),
    8: ("APT's special friend", "Be chosen."),
    9: ("eurotwelve's special friend", "Be chosen."),
    10: ("Jake's special friend", "Be chosen."),
    11: ("D4EM0N's special friend", "Be chosen."),
    12: ("Alyssa's special friend", "Be chosen."),
    13: ("Supporter", "Give back."),
    14: ("Supporter", "Give back."),
    15: ("Supporter", "Give back."),
    16: ("Supporter", "Give back."),
    17: ("Lucky number", "Get lucky."),
    18: ("Early swimmer", "Be first to the pool party."),
    19: ("Late swimmer", "Be last at the pool party."),
    20: ("Saturday mixer", "Be first at Saturday mixer."),
    21: ("Opening act", "Be first to karaoke."),
    22: ("Headliner", "Be last at karaoke."),
    23: ("Pest", "Print a lot of these."),
    24: ("Earlybird", "Print one early."),
    25: ("Weatherqueer", "Be hot and cold."),
    26: ("Eclipse", "See the light and the dark."),
    27: ("Ice", "Be cold for hours."),
    28: ("Fire", "Be hot for hours."),
    29: ("Black Tentacle", "Mate with all ubers."),
    30: ("Ruby Tentacle", "Mate with all handlers while on duty."),
    31: ("50 Tentacles", "Mate with 50."),
    32: ("100 Tentacles", "Mate with 100."),
    33: ("200 Tentacles", "Mate with 200."),
    34: ("Sprayer", "Super-ink 50 times."),
    35: ("Hanger-on", "Spend hours near an uber."),
    36: ("Handler-on", "Spend hours near a handler."),
    37: ("Controlled crowd", "Be near all on-duty handlers."),
    38: ("Mixtacular", "Attend all mixers."),
    39: ("Cheater", "Up up down down."),
    40: ("Minuteman", "Print right after turning on."),
    41: ("Switch", "Power cycle your badge a lot."),
    42: ("Super inker", "Do one super ink."),
    43: ("Dominant", "Ink a lot more than you get inked."),
    44: ("Submissive", "Get inked a lot more than you ink."),
    45: ("Vers", "Get inked and ink about the same."),
    46: ("Imposter", "Borrow a hat. Or cheat."),
    50: ("Contest", "Figure it out."),
    55: ("Uber", "Be uber."),
    56: ("Handler", "Volunteer!"),
}

hats = OrderedDict(sorted(hats_unordered.items(), key=lambda t: t[0]))

mating_format = '<BBBBHQBBBBBBH'
mating_format_nocrc = '<BBBBHQBBBBBB'
flag_format = 'p4u1u1u1u1u1u1u1u1u1u1u1p1'

MatePayloadRaw = namedtuple('MatePayloadRaw', 'proto_version from_addr hat_award_id camo_id flags achievements seen_count uber_seen_count odh_seen_count mate_count uber_mate_count odh_mate_count crc16')
Flags = namedtuple('Flags', 'f_reprint f_hat_claim_from_pipe f_pipe f_handler f_badge_has_claimed_hat f_rst f_hat_holder f_ink f_nack f_ack f_award')
MatePayload = namedtuple('MatePayload', MatePayloadRaw._fields + Flags._fields)

sync_bytes = [0xA0, 0xFF, 0x00, 0xAA]

DEDICATED_BASE_ID = 254

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
    
    return MatePayload(*(mate_payload_tuple + in_flags))

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
    badge_achievements = []
    new_hat = False
    
    result = None
    
    for i in hats.keys():
        if (payload.achievements >> i) & 1:
            badge_achievements.append(i)
    print 'Achievements:', ', '.join(map(lambda a: hats[a][0], 
                                     badge_achievements))
    
    if payload.f_hat_holder and payload.f_badge_has_claimed_hat:
        # They already have a hat, and they've actually claimed it.
        print 'They have a hat, and they have claimed it.'
    elif payload.f_hat_holder and not payload.f_badge_has_claimed_hat and payload.hat_award_id not in achievements.awarded:
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
    while True:
        p = read_payload()
        if not p:
            continue
            
        if p.f_rst:
            send_pipe_nrst()
        elif p.f_ack:
            pass # Hat accepted
        elif p.f_nack:
            pass # Hat refused. Ungrateful jackass...
        else:
            # Got a NRST, time to read achievements.
            read_and_handle_achievements(p)
