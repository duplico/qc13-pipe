import crcmod
import serial
from struct import pack, unpack
from bitstruct import pack as bitpack
from bitstruct import unpack as bitunpack

achievements_awarded = range(0,17)

hats = {
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

# typedef struct {
    # uint8_t proto_version;
    # uint8_t from_addr;
    # uint8_t hat_award_id;
    # uint8_t camo_id;
    # uint16_t flags;
    # uint64_t achievements;
    # uint8_t seen_count, uber_seen_count, odh_seen_count;
    # uint8_t mate_count, uber_mate_count, odh_mate_count;
    # uint16_t crc16;
# } matepayload;

#define M_HAT_AWARD BIT1 // Award = PUSH hat. From badge.
#define M_HAT_AWARD_ACK BIT2
#define M_HAT_AWARD_NACK BIT3
#define M_INK BIT4
#define M_HAT_HOLDER BIT5
#define M_RST BIT6
#define M_BADGE_HAS_CLAIMED_HAT BIT7 // comes from badge
#define M_HANDLER_ON_DUTY BIT8
#define M_PIPE BIT9 // 0=badge; 1=pipe
#define M_HAT_CLAIM_FROM_PIPE BITA // comes from pipe
#define M_REPRINT_HAT BITB
#define M_BESTOW_GILD BITF

# May need to pad, given the 2-byte words in MSP430.
# sync bytes: 0xA0, 0xFF, 0x00, 0xAA
#  these happen at the beginning.
# They're NOT included in this format:
# '<' = little-endian
# '>' = big-endian
mating_format = '<BBBBHQBBBBBBH'
mating_format_nocrc = '<BBBBHQBBBBBB'


# print mate_payload_tuple

sync_bytes = [0xA0, 0xFF, 0x00, 0xAA]
sync_position = 0
payload_len = 16
payload = ''

DEDICATED_BASE_ID = 254

crc_check = crcmod.mkCrcFun(0b10001000000100001, rev=False)

# When we send, f_pipe must be set, and out ID must be DEDICATED_BASE_ID

def send_pipe_claim_hat(hat_id):
    # first entry is padding...
    flags_bits = (0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    flags_bytes = bitpack('u4u1u1u1u1u1u1u1u1u1u1u1u1', *flags_bits)
    flags = ord(flags_bytes[1])
    flags += (ord(flags_bytes[0]) << 8)
    
    c = crc_check(pack(mating_format_nocrc, *(0x42, DEDICATED_BASE_ID, 0xff, 0, flags, 0x00, 0, 0, 0, 0, 0, 0))
    out_payload = pack(mating_format, 0x42, DEDICATED_BASE_ID, 0xff, 0, flags, 0x00, 0, 0, 0, 0, 0, 0, c)
    
    # TX: sync_bytes
    ser.write(map(chr, sync_bytes))
    # TX: out_payload
    ser.write(out_payload)

def send_pipe_nrst():
    flags_bits = (0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    flags_bytes = bitpack('u4u1u1u1u1u1u1u1u1u1u1u1u1', *flags_bits)
    flags = ord(flags_bytes[1])
    flags += (ord(flags_bytes[0]) << 8)

    c = crc_check(pack(mating_format_nocrc, *(0x42, DEDICATED_BASE_ID, 0xff, 0, flags, 0x00, 0, 0, 0, 0, 0, 0))
    out_payload = pack(mating_format, 0x42, DEDICATED_BASE_ID, 0xff, 0, flags, 0x00, 0, 0, 0, 0, 0, 0, c)
    
    # TX: sync_bytes
    ser.write(map(chr, sync_bytes))
    # TX: out_payload
    ser.write(out_payload)

def handle_input(payload):
    mate_payload_tuple = unpack(mating_format, payload)
    (proto_version,
     from_addr,
     hat_award_id,
     camo_id,
     flags,
     achievements,
     seen_count, uber_seen_count, odh_seen_count,
     mate_count, uber_mate_count, odh_mate_count,
     crc16) = mate_payload_tuple
    c = crc_check(pack(mating_format_nocrc, proto_version, from_addr, hat_award_id, camo_id, flags, achievements, seen_count, uber_seen_count, odh_seen_count, mate_count, uber_mate_count, odh_mate_count))
    if c != crc16:
        print 'bad!'
        return
    
    flags0 = flags & 0xFF
    flags1 = (flags & 0xFF00) >> 8
    
    (f_pad, f_reprint, f_hat_claim_from_pipe,
     f_pipe, f_handler, f_badge_has_claimed_hat, f_rst,
     f_hat_holder, f_ink, f_nack, f_ack, f_award,
     f_unused) = bitunpack('u4u1u1u1u1u1u1u1u1u1u1u1u1', [flags1, flags0])
    
    # So first we receive a RST from the badge. That's how we start our interaction
    #  with it. 
    # Then we send a message with ~RST and f_pipe and id=DEDICATED_BASE_ID
    #  Badge then enters MS_PIPE_PAIRED
    
    # Send ~RST
    send_pipe_nrst()
    
    # Now! The badge is right where we want it.
    
    badge_achievements = []
    ach = achievements
    
    new_hat = False
    
    # Let's go ahead and read its achievements.
    
    for i in range(57):
        if ach & 1:
            badge_achievements.append(i)
        ach = ach >> 1
        
    if f_hat_holder and f_badge_has_claimed_hat:
        pass
    elif f_hat_holder and not f_badge_has_claimed_hat:
        # TIME TO AWARD IT, WOOOOOOOOO!!!!
        pass
    else:
        # Let's find an unawarded ACHIEVEMENT!
        for achievement in ach[::-1]: # Work backwards.
            if achievement not in achievements_awarded and achievement in hats:
                # It's available!
                send_pipe_claim_hat(achievement)
                new_hat = True
                break
        
    # Print a receipt.
    print mate_payload_tuple
    print 'id %d with hat %d' % (from_addr, hat_award_id)
    # Done.


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
            handle_input(payload)
            payload = ''
            sync_position = 0
        else:
            payload += in_byte
