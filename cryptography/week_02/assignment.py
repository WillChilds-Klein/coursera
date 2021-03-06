from Crypto.Cipher import AES

BLOCK_SIZE_BYTES = 16

KEY_CBC = '140b41b22a29beb4061bda66b6747e14'
KEY_CTR = '36f18357be4dbd77f050515c73fcf9f2'

CT_CBC_0 = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'
CT_CBC_1 = '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'
CT_CTR_0 = '69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'
CT_CTR_1 = '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'


def strxor(a, b):
    def xor(p, q):
        assert len(p) == len(q)
        chars = [chr(ord(x) ^ ord(y)) for (x, y) in zip(p, q)]
        return ''.join(chars).encode('hex')
    if len(a) > len(b):
        return xor(a[:len(b)].decode('hex'), b.decode('hex'))
    else:
        return xor(a.decode('hex'), b[:len(a)].decode('hex'))

def strip_iv(text):
    iv_length = BLOCK_SIZE_BYTES * 2  # 2 hex digits per byte
    assert len(text) >= iv_length
    return (text[:iv_length], text[iv_length:])

def pad(inpt):
    size = BLOCK_SIZE_BYTES - (len(inpt)/2) % BLOCK_SIZE_BYTES
    return inpt + ''.join([chr(size).encode('hex') for _ in range(size)])

def unpad(inpt):
    last = inpt[-2:]
    return inpt[:-1*2*int(last, base=16)]       # 2 hex digits per byte

def cbc_encrypt(inpt):
    iv, pts = strip_iv(inpt)
    block_chars = BLOCK_SIZE_BYTES * 2
    pts = pad(pts)
    pts = [pts[i:i+block_chars] for i in range(0, len(inpt), block_chars)]
    cipher = AES.new(KEY_CBC.decode('hex'), AES.MODE_ECB)
    cts = []
    prev = iv
    for p in pts:
        c = strxor(p, prev)
        c = cipher.encrypt(c.decode('hex')).encode('hex')
        cts.append(c)
        prev = c
    return iv + ''.join(cts)

def cbc_decrypt(inpt):
    iv, cts = strip_iv(inpt)
    block_chars = BLOCK_SIZE_BYTES * 2
    cts = [cts[i:i+block_chars] for i in range(0, len(inpt), block_chars)]
    cipher = AES.new(KEY_CBC.decode('hex'), AES.MODE_ECB)
    pts = []
    prev = iv
    for c in cts:
        p = cipher.decrypt(c.decode('hex')).encode('hex')
        pts.append(strxor(p, prev))
        prev = c
    return iv + unpad(''.join(pts))

def ctr_increment(ctr):
    # TODO: right now, this only increments the final byte...
    #       i.e. it's only secure for 256 messages for a given key :(
    prfx = ctr[:len(ctr)-2]
    return prfx + chr(ord(ctr[len(ctr)-2:].decode('hex'))+1).encode('hex')

def ctr_encrypt(inpt):
    iv, pts = strip_iv(inpt)
    block_chars = BLOCK_SIZE_BYTES * 2
    pts = [pts[i:i+block_chars] for i in range(0, len(inpt), block_chars)]
    cipher = AES.new(KEY_CTR.decode('hex'), AES.MODE_ECB)
    cts = []
    ctr = iv
    for p in pts:
        enc = cipher.encrypt(ctr.decode('hex')).encode('hex')
        cts.append(strxor(enc, p))
        ctr = ctr_increment(ctr)
    return iv + ''.join(cts)

def ctr_decrypt(inpt):
    iv, cts = strip_iv(inpt)
    block_chars = BLOCK_SIZE_BYTES * 2
    cts = [cts[i:i+block_chars] for i in range(0, len(inpt), block_chars)]
    cipher = AES.new(KEY_CTR.decode('hex'), AES.MODE_ECB)
    pts = []
    ctr = iv
    for c in cts:
        enc = cipher.encrypt(ctr.decode('hex')).encode('hex')
        pts.append(strxor(enc, c))
        ctr = ctr_increment(ctr)
    return iv + ''.join(pts)

def main():
    print 'CBC_0: ' + strip_iv(cbc_decrypt(CT_CBC_0))[1].decode('hex')
    print 'CBC_1: ' + strip_iv(cbc_decrypt(CT_CBC_1))[1].decode('hex')
    print 'CTR_0: ' + strip_iv(ctr_decrypt(CT_CTR_0))[1].decode('hex')
    print 'CTR_1: ' + strip_iv(ctr_decrypt(CT_CTR_1))[1].decode('hex')

    assert CT_CBC_0 == cbc_encrypt(cbc_decrypt(CT_CBC_0))
    assert CT_CBC_1 == cbc_encrypt(cbc_decrypt(CT_CBC_1))
    assert CT_CTR_0 == ctr_encrypt(ctr_decrypt(CT_CTR_0))
    assert CT_CTR_1 == ctr_encrypt(ctr_decrypt(CT_CTR_1))


if __name__ == '__main__':
    main()
