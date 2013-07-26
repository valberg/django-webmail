from Crypto.Cipher import ARC4
from base64 import b64encode, b64decode
from os import urandom

from django.conf import settings

SALT_SIZE = 8

def encrypt(plaintext):
    salt = urandom(SALT_SIZE)
    arc4 = ARC4.new(salt + settings.SECRET_KEY)
    plaintext = "{:3d}{}{}".format(
        len(plaintext), plaintext, urandom(256-len(plaintext))
    )

    return "%s$%s" % (b64encode(salt), b64encode(arc4.encrypt(plaintext)))

def decrypt(ciphertext):
    salt, ciphertext = map(b64decode, ciphertext.split('$'))
    arc4 = ARC4.new(salt + settings.SECRET_KEY)
    plaintext = arc4.decrypt(ciphertext)

    return plaintext[3:3+int(plaintext[:3].strip())]
