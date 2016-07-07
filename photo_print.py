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
pidfile = "/tmp/qc13pipe.pid"

if os.path.isfile(pidfile):
    print "%s already exists, exiting" % pidfile
    sys.exit()
else:
    file(pidfile, 'w').write(pid)

at = Adafruit_Thermal()

at.println("     Happy Queercon")
at.println("")
at.println("")
at.println("")

os.unlink(pidfile)
