import hashlib, hmac

secret1 = "aawej123fnlkwjenlASEFAESFZlekjfnwelfhuw3rAWEFq23wqw32rr3q23aroefDSfA111"
secret2 = "awefawefawrfaw2342342323453SAeLAIWENFAILSEKlk132qelkm"

def hash(passphrase):
    h1 = hmac.new(str(secret1 + passphrase)).hexdigest()
    h2 = hmac.new(str(passphrase + secret2)).hexdigest()
    return h1 + h2