# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

class encrypt_rsa():

    def __init__(self):
        """ init """
        # 密钥长度, 明文最大长度, 密文长度
        rsa_config = (1024,  86, 128)
        # rsa_config = (2048, 214, 256)

        private_key = RSA.generate(rsa_config[0])
        public_key = private_key.publickey()

        # private_key_bytes & public_key_bytes
        self.privkey = private_key.export_key()
        self.pubkey = public_key.export_key()

        self._public_cipher = PKCS1_OAEP.new(public_key)
        self._private_cipher = PKCS1_OAEP.new(private_key)

        # 加密长度
        self._encrypt_len = rsa_config[1]
        # 解密长度
        self._rsaDecrypt_len = rsa_config[2]
        # 公钥加密对象字典
        self._public_cipher_dict = {}

    def _cut(self, obj, sec):

        return [obj[i:i+sec] for i in range(0,len(obj),sec)]

    def encrypt(self, info: bytes):

        crypto = b""
        for line in self._cut(info, self._encrypt_len):
            crypto += self._public_cipher.encrypt(line)

        return crypto

    def encrypt_user(self, info: bytes, pubkey: str):

        try:
            public_cipher = self._public_cipher_dict[pubkey]
        except KeyError:
            public_cipher = PKCS1_OAEP.new(RSA.import_key(pubkey))
            self._public_cipher_dict[pubkey] = public_cipher

        crypto = b""
        for line in self._cut(info, self._encrypt_len):
            crypto += public_cipher.encrypt(line)

        return crypto

    def decrypt(self, info: bytes):

        content = b""
        for line in self._cut(info, self._rsaDecrypt_len):
            content += self._private_cipher.decrypt(line)

        return content

class encrypt_aes():

    def __init__(self, key: str=None, iv: str=None):
        """ init """
        if key:
            self.key = key.encode()
        else:
            self.key = get_random_bytes(16)
        if iv:
            self.iv = iv.encode()
        else:
            self.iv = get_random_bytes(16)

        self.block_size = 16

        # 反填充函数，去除填充的字符
        self.unpad = lambda s: s[0:-s[-1]]

    def pad(self, text: bytes):
        """ PKCS5Padding 填充，使被加密数据的字节码长度是 block_size 的整数倍 """
        count = len(text)
        add_num = self.block_size - (count % self.block_size)
        entext = text + (chr(add_num).encode() * add_num)

        return entext

    def encrypt(self, info: bytes):

        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        res = aes.encrypt(self.pad(info))

        return res

    def encrypt_user(self, info: bytes, key: bytes, iv: bytes):

        aes = AES.new(key, AES.MODE_CBC, iv)
        res = aes.encrypt(self.pad(info))

        return res

    def decrypt(self, info: bytes):

        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        content = self.unpad(aes.decrypt(info))

        return content