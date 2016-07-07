import base64

import qrcode
from M2Crypto.EVP import hmac

KEY = 'iSLJVA4c5TmIM103GHPWM6fz5NIHnGuAPU0x8t6UxyWi1F6wulrJilkbqk7cgma'

def get_url(badge_id, award_id):
    award = badge_id*256+award_id
    code = hmac(KEY, '%d' % award)
    award_64 = base64.b64encode(str(award), "-_").strip()
    code_64 = base64.b64encode(code, "-_").strip()
    url = "duplico.webfactional.com/h/%s/%s" % (award_64, code_64)
    return url
    
if __name__ == "__main__":
    url = get_url(100, 40)
    print url
    qimage = qrcode.make(url)
    qimage.show()
    