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
at.begin(255)
at.setTimes(35000,1000)

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
    qimage = qrcode.make(url)
    (width, height) = qimage.size
    qimage.thumbnail((384,384))
    centered_image = Image.new('1', (384,128), 1)
    centered_image.paste(qimage, box=(128,0))
    centered_image = qimage

    at.println("   your journey so far")
    header = Image.open('qc13receiptlogo2.png')
    header.thumbnail((384,384))
    at.printImage(header, LaaT=True)
    at.println('''             |_  _ _ 
       ***|_||_)(-| ***''')
    at.println("        swam near |----00/15---|")
    at.println("touched tentacles |----00/15---|")
    at.println("   sprayed by ink |****00/15***|")
    at.println("   sprayed as one |****00/15***|")
    at.println('''       |_  _  _  _|| _ _ 
       | )(_|| )(_||(-|  ''')
    at.println("        swam near |****00/15***|")
    at.println("touched tentacles |****00/15***|")
    at.println("   sprayed by ink |****00/15***|")
    at.println("   sprayed as one |****00/15***|")
    at.println('''        |_     _  _  _  
        | )|_||||(_|| )''')
    at.println("        swam near |*--001/250--|")
    at.println("touched tentacles |*--001/250--|")
    at.println("   sprayed by ink |*--001/250--|")
    at.println("   sprayed as one |*--001/250--|")
    at.println('''    _ _  _  _    r | _  _  _ 
   (_(_||||(_)|_|| |(_|(_)(- 
                     _|''')
    at.println("aqua | fire | rainbow | electricity")
    at.println('''   _  _|_ . _   _ _  _ _ |_ _ 
  (_|(_| )|(-\/(-|||(-| )|__) ''')
    at.println("AWESOME")
    at.println("COLD DAYS")
    at.println('''                 ___ 
          |__| /\ |  
          |  |/--\|  
             __  __    __ __  
 /  \|\ ||  /  \/  |_/|_ |  \ 
 \__/| \||__\__/\__| \|__|__/ ''')
    at.printImage(centered_image, LaaT=True)
    at.println('   find a hat handing handler.')
    at.println('')

    os.unlink(pidfile)

    
