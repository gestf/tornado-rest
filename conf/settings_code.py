#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
错误码配置
"""

# 系统错误码
E_SUCC, E_PARAM, E_INTER, E_EXTERNAL = 0, 1, 2, 3
E_TIMEOUT, E_RESRC, E_AUTH, E_FORBIDDEN = 4, 5, 6, 7

# 错误码描述
ERR_DESC = {
    # 基本错误码
    E_SUCC: "成功",
    E_PARAM: "参数错误",
    E_INTER: "程序内部错误",
    E_EXTERNAL: "外部接口错误",
    E_TIMEOUT: "第三方接口超时",
    E_RESRC: "接口不存在",
    E_AUTH: "鉴权失败",
    E_FORBIDDEN: "访问被禁止"
}
