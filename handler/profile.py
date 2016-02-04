#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用户资料API处理器
"""
from conf.status_code import E_SUCC
from rest.base import route, RestHandler


class ProfileHandler(RestHandler):
    """
    账户类API处理器
    """
    @route(method='GET', module="test")
    def get_test(self):
        """
        统一接口处理器
        """
        self.send_result(E_SUCC)
