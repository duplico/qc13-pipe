import os
import sys
import base64
import serial

from PIL import Image, ImageEnhance

import qrcode
from M2Crypto.EVP import hmac

from Adafruit_Thermal import Adafruit_Thermal

pid = str(os.getpid())
pidfile = "/tmp/qc13pipe.pid"

KEY = 'iSLJVA4c5TmIM103GHPWM6fz5NIHnGuAPU0x8t6UxyWi1F6wulrJilkbqk7cgma'

at = Adafruit_Thermal()

def get_url(badge_id, award_id):
    award = badge_id*256+award_id
    code = hmac(KEY, '%d' % award)
    award_64 = base64.b64encode(str(award), "-_").strip()
    code_64 = base64.b64encode(code, "-_").strip()
    url = "badge.lgbt/h/%s/%s" % (award_64, code_64)
    return url
    
if __name__ == "__main__":
    if os.path.isfile(pidfile):
        print "%s already exists, exiting" % pidfile
        sys.exit()
    else:
        file(pidfile, 'w').write(pid)
    url = get_url(100, 40)
    print url
    qimage = qrcode.make(url)
    (width, height) = qimage.size
    qimage.thumbnail((384,384))
#    centered_image = Image.new('1', (384,128), 1)
#    centered_image.paste(qimage, box=(128,0))
    centered_image = qimage

    at.printImage(centered_image, LaaT=False)
    at.println(url)
    at.println(qimage.mode)
    at.println("")
    at.println("")
    os.unlink(pidfile)

    
