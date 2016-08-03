from collections import namedtuple, OrderedDict, defaultdict

MatePayloadRaw = namedtuple('MatePayloadRaw', 'proto_version from_addr hat_award_id camo_id flags achievements seen_count uber_seen_count odh_seen_count mate_count uber_mate_count odh_mate_count crc16')
Flags = namedtuple('Flags', 'f_reprint f_hat_claim_from_pipe f_pipe f_handler f_badge_has_claimed_hat f_rst f_hat_holder f_ink f_nack f_ack f_award')
MatePayload = namedtuple('MatePayload', MatePayloadRaw._fields + Flags._fields + ('achievement_list',))

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

camos_all = {
    0: ("Newbie", "The starting camo."),
    1: ("Doubleinker", "Discover super inking."),
    2: ("Fire", "Send 20 inks."),
    3: ("Found", "Attend QC trans meetup."),
    4: ("Gamer", "^ ^ v v < > < > B A START."),
    5: ("Geek Girl", "Attend Women of QC."),
    6: ("Giver", "Donate before the con."),
    7: ("Glam", "Mate with an uber."),
    8: ("Handler", "Be a handler."),
    9: ("QC HAT", "Earn a hat!"),
    10: ("Karate Kid", "Send 50 inks."),
    11: ("Learned", "Attend QC badge talk."),
    12: ("Lush", "Mate with 10 badges."),
    13: ("Mixologist", "Attend a mixer."),
    14: ("Partytime", "Attend Saturday event."),
    15: ("Rainbow", "Attend the pool party."),
    16: ("Power hungry", "Mate with all handlers."),
    17: ("Cold days", "Freeze your badge."),
    18: ("Short circuit", "Be Jason."),
    19: ("Uber", "Be uber."),
    20: ("Wrap-up 1", "Make it to Sunday."),
    21: ("Wrap-up 2", "Do some stuff before Sunday."),
    22: ("Wrap-up 3", "Do a lot before Sunday."),
    23: ("Wrap-up 4", "Be awesome by Sunday."),
    24: ("Bear flag", "Be inked by this flag."),
    25: ("Bi flag", "Be inked by this flag."),
    26: ("Leather flag", "Be inked by this flag."),
    27: ("Trans flag", "Be inked by this flag."),
}

camos = defaultdict(lambda a: ('???', 'Break the pipe.'), **camos_all)

DEDICATED_BASE_ID = 254
STAR_WIDTH = 12    
UBER_COUNT = 13
HANDLER_COUNT = 8
