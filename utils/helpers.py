from Crypto.Cipher import AES
from django.conf import settings
import base64


def get_host(request):
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'
    return protocol + request.get_host()


def encrypt(astring):
    encryption_suite = AES.new(settings.AES_KEY, AES.MODE_CBC, 'This is an IV456')
    cipher_text = base64.b64encode(encryption_suite.encrypt(astring.rjust(16))).decode()
    return cipher_text


def decrypt(astring):
    decryption_suite = AES.new(settings.AES_KEY, AES.MODE_CBC, 'This is an IV456')
    plain_text = decryption_suite.decrypt(base64.b64decode(astring))
    return plain_text.strip()
