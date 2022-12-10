#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import uuid
import hashlib
import datetime
import base64
import random
import string
import traceback
from Crypto.Cipher import AES
from conf.paths import LICENSE_PATH
from libs.logger import logger


def get_mac():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def hashed(msg):
    sha256 = hashlib.sha256()
    sha256.update(msg.encode('utf-8'))
    res = sha256.hexdigest()
    return res


class AESHelper(object):
    def __init__(self, password, iv):
        self.password = bytes(password, encoding='utf-8')
        self.iv = bytes(iv, encoding='utf-8')

    @staticmethod
    def pkcs7padding(text):
        """
        明文使用PKCS7填充
        最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
        :param text: 待加密内容(明文)
        :return:
        """
        bs = AES.block_size  # 16
        length = len(text)
        bytes_length = len(bytes(text, encoding='utf-8'))
        # tips：utf-8编码时，英文占1个byte，而中文占3个byte
        padding_size = length if(bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
        padding_text = chr(padding) * padding
        return text + padding_text

    @staticmethod
    def pkcs7unpadding(text):
        """
        处理使用PKCS7填充过的数据
        :param text: 解密后的字符串
        :return:
        """
        length = len(text)
        unpadding = ord(text[length-1])
        return text[0:length-unpadding]

    def encrypt(self, content):
        """
        AES加密
        模式cbc
        填充pkcs7
        :param content: 加密内容
        :return:
        """
        cipher = AES.new(self.password, AES.MODE_CBC, self.iv)
        content_padding = self.pkcs7padding(content)
        encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result

    def decrypt(self, content):
        """
        AES解密
        模式cbc
        去填充pkcs7
        :param content:
        :return:
        """
        cipher = AES.new(self.password, AES.MODE_CBC, self.iv)
        encrypt_bytes = base64.b64decode(content)
        decrypt_bytes = cipher.decrypt(encrypt_bytes)
        result = str(decrypt_bytes, encoding='utf-8')
        result = self.pkcs7unpadding(result)
        return result


random.seed(100)
candidates = string.digits+string.ascii_letters
# AttributeError: module 'random' has no attribute 'choices'
# _secret = ''.join(random.choices(string.digits+string.ascii_letters, k=16))  # 密钥
_secret = ''.join([random.choice(candidates) for i in range(16)])  # 密钥
random.seed(200)
# _iv = ''.join(random.choices(string.digits+string.ascii_letters, k=16))      # 偏移量
_iv = ''.join([random.choice(candidates) for i in range(16)])


class LicenseHelper(object):
    def __init__(self):
        self.aes = AESHelper(_secret, _iv)
        self.license_path = LICENSE_PATH

    def generate(self, user='default', mac=get_mac(), end_date=None):
        if os.path.exists(self.license_path):
            return
        if not end_date:
            # 默认30天试用期
            end_date = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        psw = hashed('mozi' + str(mac))
        license_dict = {'user': user, 'psw': psw, 'end_date': end_date, 'mac': mac}
        license_result = self.aes.encrypt(str(license_dict))
        with open(self.license_path, 'w') as fopen:
            fopen.write(license_result)
        return license_result

    def load(self):
        with open(self.license_path) as fopen:
            license_result = fopen.read()
        lic_msg = bytes(license_result, encoding='utf8')
        license_str = self.aes.decrypt(lic_msg)
        license_dict = eval(license_str)
        return license_dict

    @staticmethod
    def _check_date(lic_date):
        cur_date = datetime.datetime.now()
        end_date = datetime.datetime.strptime(lic_date, '%Y-%m-%d')
        remain_date = end_date - cur_date
        if remain_date.days < 0:
            return False
        return True

    @staticmethod
    def _check_psw(psw):
        mac_addr = get_mac()
        hashed_msg = hashed('mozi' + str(mac_addr))
        if psw == hashed_msg:
            return True
        return False

    def check(self):
        try:
            license_dict = self.load()
        except FileNotFoundError:
            return 'License文件不存在，请将有效License文件放置在于目录%s下' % os.path.dirname(LICENSE_PATH)
        except:
            logger.error(traceback.format_exc())
            return '无效的License，请联系工作人员'
        #
        if not self._check_date(license_dict['end_date']):
            return 'License有效期至：%s(已到期)，请联系工作人员' % license_dict['end_date']
        # if not self._check_psw(license_dict['psw']):
        #     return 'MAC地址发生变化，请联系工作人员'
        return 'OK'


if __name__ == '__main__':
    # print(get_mac())
    helper = LicenseHelper()
    lic = helper.generate()
    # print(lic)
    # print(helper.load())
    print(helper.check())
