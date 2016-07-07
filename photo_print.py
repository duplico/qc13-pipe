import pickle
import os
import sys
import datetime

from StringIO import StringIO
from datetime import datetime

import serial
from PIL import Image, ImageEnhance

from Adafruit_Thermal import Adafruit_Thermal

pid = str(os.getpid())
pidfile = "/tmp/photoprint.pid"

if os.path.isfile(pidfile):
    print "%s already exists, exiting" % pidfile
    sys.exit()
else:
    file(pidfile, 'w').write(pid)

at = Adafruit_Thermal()

PHOTO_DIRECTORY = '/mnt/db/photobooth'
PHOTO_LISTING = '/mnt/db/photobooth/list.pickle'

if not os.path.exists(PHOTO_LISTING):
    previous_files = set()
    pickle.dump(previous_files, open(PHOTO_LISTING, 'w+'))
else:
    previous_files = pickle.load(open(PHOTO_LISTING, 'r'))

i_printed = False

for path in (
        os.path.join(PHOTO_DIRECTORY, fname) for fname \
        in os.listdir(PHOTO_DIRECTORY) if fname.endswith('.jpg')
):
    if path not in previous_files:
        i_printed = True
        print path
        image = Image.open(path)
        (width, height) = image.size

        if width > height:
            image = image.rotate(90, expand=True)

        (width, height) = image.size

        if width > 384:
            image = image.resize((384, height - (width - 384)), Image.NEAREST)

        colorer = ImageEnhance.Color(image)
        sharpener = ImageEnhance.Sharpness(colorer.enhance(0))
        image = sharpener.enhance(2.0)
        contraster = ImageEnhance.Contrast(image)
        at.printImage(contraster.enhance(2.0), LaaT=True)
        previous_files.add(path)
        at.println("     Happy Halloween %d" % datetime.date.today().year)
        at.println("")
        at.println("")

if i_printed == True:
    at.println("")
    at.println("")
    at.println("")

pickle.dump(previous_files, open(PHOTO_LISTING, 'w'))
os.unlink(pidfile)
