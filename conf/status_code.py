#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
错误码配置
"""

# 系统错误码
E_SUCC, E_PARAM, E_INTER, E_EXTERNAL = 0, 1, 2, 3
E_TIMEOUT, E_RESRC, E_AUTH, E_FORBIDDEN = 4, 5, 6, 7
E_RESOURCE_NOT_FIND = 8

# 用户模块 1000 - 2000
E_USER_LOCKED = 1000
E_USER_EXIST = 1001
E_USER_NOT_EXIST = 1002
E_USER_LOGIN = 1003
E_USER_NOT_LOGIN = 1004
E_USER_NAME_OR_PWD_ERROR = 1005
E_USER_VERIFY_CODE_LOCKED = 1006
E_USER_VERIFY_CODE_ERROR = 1007

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
    E_FORBIDDEN: "访问被禁止",
    E_RESOURCE_NOT_FIND: "资源不存在或已删除",

    # 用户模块
    E_USER_LOCKED: "用户被锁定",
    E_USER_EXIST: "用户已存在",
    E_USER_NOT_EXIST: "用户不存在",
    E_USER_LOGIN: "用户已登录",
    E_USER_NOT_LOGIN: "用户未登录",
    E_USER_NAME_OR_PWD_ERROR: "用户名或者密码错误",
    E_USER_VERIFY_CODE_LOCKED: "请不要在60秒内连续发送验证码",
    E_USER_VERIFY_CODE_ERROR: "您提供的验证码错误，请检查后重新输入",
}