#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
开发环境配置
"""
import mongoengine

REDIS_CNF = {
    "session": {
        "host": "192.168.1.16",
        "port": 6379,
        "db": 0,
    },
}

DB_IP_ADDRESS = '192.168.1.16'
mongoengine.connect('gezi', host=DB_IP_ADDRESS, alias="gezi")