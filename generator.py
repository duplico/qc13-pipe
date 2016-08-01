import os
import sys
import base64
import serial
from textwrap import wrap

from PIL import Image, ImageEnhance

import qrcode
from M2Crypto.EVP import hmac

from Adafruit_Thermal import Adafruit_Thermal
from qc13conf import *

pid = str(os.getpid())
pidfile = "/tmp/qc13pipe.pid"

KEY = 'iSLJVA4c5TmIM103GHPWM6fz5NIHnGuAPU0x8t6UxyWi1F6wulrJilkbqk7cgma'

at = Adafruit_Thermal()
at.begin(255)
at.setTimes(35000,1000)

def get_url(badge_id, award_id):
    award = badge_id*256+award_id
    code = hmac(KEY, '%d' % award)
    award_64 = base64.b64encode(str(award), "-_").strip()
    code_64 = base64.b64encode(code, "-_").strip()
    url = "badge.lgbt/h/%s/%s" % (award_64, code_64)
    return url
    
def progress_bar(label, amt, outof):
    star_count = int((1.0/STAR_WIDTH)*amt/outof)
    if amt == outof: # Make sure it's full irrespective of rounding
        star_count = STAR_WIDTH
    elif star_count == STAR_WIDTH: # Not complete but full:
        star_count = STAR_WIDTH-1 # Don't show it as full.
    elif amt and not star_count: # Show 1 * if any, regardless of rounding
        star_count = 1
    
    out = ' '*(17-len(label))
    out += label
    out += ' |'
    
    bar = '*'*star_count
    bar += '-'*(STAR_WIDTH-star_count)
    
    wid = len(str(outof))
    number = '%s/%d' % (str(amt).zfill(wid), outof)
    
    # So we need to cut out the middle len(number) chars from bar.
    # new_bar_len = STAR_WIDTH-len(number)
    # So half_len = (STAR_WIDTH-len(number))/2
    
    out += bar[:(STAR_WIDTH-len(number))/2]
    out += number
    out += bar[((STAR_WIDTH-len(number))/2 + len(number)):]
    
    out += '|'
    
    return out

ROW_SPACE = 15

def print_img(path):
    i = Image.open(path)
    i.thumbnail((384,384))
    at.printImage(i, LaaT=True)
    

def print_journey(badge, print_code):
    if badge.f_reprint and badge.f_hat_holder:
        print_code = badge.hat_award_id
    at.justify('L')
    if print_code is not None:
        print 'We should print a QR code.'
    
    at.println("   your journey so far") #    (%d)" % badge.from_addr)
    print_img('qc13receiptlogo_smw.png')
    print_img('uber.png')
    at.println(progress_bar('been near', badge.uber_seen_count, UBER_COUNT))
    at.println(progress_bar('touched tentacles', badge.uber_mate_count, UBER_COUNT))
    
    at.feedRows(ROW_SPACE)
    print_img('handler.png')
    at.println(progress_bar('been near', badge.odh_seen_count, HANDLER_COUNT))
    at.println(progress_bar('touched tentacles', badge.odh_mate_count, HANDLER_COUNT))
    
    at.feedRows(ROW_SPACE)
    print_img('blooper.png')
    at.println(progress_bar('been near', badge.seen_count, 250))
    at.println(progress_bar('touched tentacles', badge.mate_count, 250))
    
    at.feedRows(ROW_SPACE)
    print_img('camo.png')
    at.justify('C')
    at.underlineOn()
    at.println(camos[badge.camo_id][0])
    at.underlineOff()
    for line in wrap(camos[badge.camo_id][1], 32):
        at.println(line)
    
    at.feedRows(ROW_SPACE)
    print_img('achievements.png')
    
    ach_list = map(lambda a: hats[a][0], badge.achievement_list)
    ach_text = ' | '.join(ach_list)
    for line in wrap(ach_text, 32):
        at.println(line)
    
    at.justify('L')
    at.feedRows(ROW_SPACE)
    
    if badge.f_hat_holder:
        print_img('hat.png')
        at.underlineOn()
        at.justify('C')
        at.println(hats[badge.hat_award_id][0])
        at.underlineOff()
        for line in wrap(hats[badge.hat_award_id][1], 32):
            at.println(line)
        at.justify('L')
    
    if print_code is not None:
        at.feedRows(ROW_SPACE)
        url = get_url(badge.from_addr, print_code)
        qimage = qrcode.make(url)
        (width, height) = qimage.size
        qimage.thumbnail((384,384))
        centered_image = Image.new('1', (384,128), 1)
        centered_image.paste(qimage, box=(128,0))
        centered_image = qimage
        at.printImage(centered_image, LaaT=True)
        print_img('unlock.png')
        at.justify('C')
        at.println('find a handler.')
        if badge.f_reprint: at.println('(reprint)')
        at.justify('L')
    at.feed(3)    
    
if __name__ == "__main__":
    if os.path.isfile(pidfile):
        print "%s already exists, exiting" % pidfile
        sys.exit()
    else:
        file(pidfile, 'w').write(pid)
        
    os.unlink(pidfile)
    

    
