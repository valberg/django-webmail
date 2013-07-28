'''
Stolen from https://github.com/mtigas/django-twofactor/blob/master/django_twofactor/encutil.py
'''

from os import urandom
from django.conf import settings
import string
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto.Hash import SHA256


def _gen_salt(length=16):
    return u''.join(
        [random.choice(string.letters + string.digits) for i in range(length)]
    )


def _get_key(salt):
    """ Combines `settings.SECRET_KEY` with a salt. """
    if not salt:
        salt = ""

    return SHA256.new('{}{}'.format(settings.SECRET_KEY, salt)).digest()


def encrypt(text):
    salt = _gen_salt()
    aes = AES.new(_get_key(salt), AES.MODE_ECB)
    plaintext = "{:3d}{}{}".format(
        len(text), text, urandom(29 - len(text))
    )

    return "{}${}".format(b64encode(salt), b64encode(aes.encrypt(plaintext)))


def decrypt(ciphertext):
    salt, ciphertext = map(b64decode, ciphertext.split('$'))
    aes = AES.new(_get_key(salt), AES.MODE_ECB)
    plaintext = aes.decrypt(ciphertext)

    return plaintext[3:3 + int(plaintext[:3].strip())]
