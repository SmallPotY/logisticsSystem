# -*- coding:utf-8 -*-
import hashlib, base64, random, string


class StringTools:

    @staticmethod
    def get_md5_string(key):
        """
        返回md5加密字符串
        :param key: 加密字符
        """
        m = hashlib.md5()
        m.update(bytes(key, 'ascii'))
        sign = m.hexdigest().upper()
        return sign

    @staticmethod
    def get_random_string(length=16):
        """
        返回随机字符串
        :param length: 字符串长度,默认16
        """
        key_list = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return "".join(key_list)


if __name__ == '__main__':
    pass
