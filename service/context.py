#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全局资源上下文
"""
import redis
import string
import random
import logging
from conf.settings import REDIS_CNF


class Singleton(object):
    """
    单例类
    """
    _instance = None

    def __new__(cls, *args, **kargs):
        """
        真正的 "构造" 函数
        """
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kargs)
        return cls._instance


class Context(object):
    """
    全局资源上下文
    """
    def __init__(self):
        """
        初始化全局变量
        """
        # session存储redis
        self.session_redis = redis.Redis(host=REDIS_CNF["session"]["host"],
                                         port=REDIS_CNF["session"]["port"],
                                         db=REDIS_CNF["session"]["db"])

    @staticmethod
    def inst():
        """
        单例
        """
        name = "_instance"
        if not hasattr(Context, name):
            setattr(Context, name, Context())
        return getattr(Context, name)

    @staticmethod
    def gen_random_code(length, with_letters=False):
        """
        生成指定长度的随即码
        @len: 长度
        return open_code
        """
        digits = string.digits
        if with_letters:
            digits += string.uppercase.replace("O", "")
            digits = digits.replace("0", "").replace("I", "")
            digits = digits.replace("1", "").replace("D", "")
            digits = digits.replace("G", "").replace("J", "")
            digits = digits.replace("M", "").replace("R", "")
            digits = digits.replace("T", "")
        return "".join(random.sample(digits, length))




