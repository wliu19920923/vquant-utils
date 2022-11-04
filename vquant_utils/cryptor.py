import base64
from Crypto.Cipher import DES3


def abstract(text):
    return '%s****%s' % (text[:2], text[-2:])


def des3encrypt(key, text):
    aes = DES3.new(key, DES3.MODE_ECB)
    count = len(text.encode('utf8'))
    add = DES3.block_size - (count % DES3.block_size)
    text = text + (chr(add) * add)
    res = aes.encrypt(text.encode('utf8'))
    msg = str(base64.b64encode(res), encoding='utf8')
    return msg


def des3decrypt(key, text):
    aes = DES3.new(key, DES3.MODE_ECB)
    res = base64.decodebytes(text.encode('utf8'))
    msg = aes.decrypt(res).decode('utf8')
    return msg[0:-ord(msg[-1])]