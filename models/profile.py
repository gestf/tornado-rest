#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
models for users api.
"""
import gsdb
import datetime
from mongoengine import *


@gsdb.change_lut_on_save
class Profile(Document):
    """
    Telephone verification code.
    """
    meta = {"db_alias": "gezi",
            "indexes": ["user_id", "user_name"]}

    user_id = StringField(required=True, unique=True)
    user_name = StringField(required=True)
    password = StringField()
    created = DateTimeField(default=datetime.datetime.now)
    lut = DateTimeField(default=datetime.datetime.now)

