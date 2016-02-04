#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基础配置
"""
import socket
from tornado.options import define, options

DEBUG = options.debug

MODEL_ENGINE = "rest.backends.mongo"

# 日志主目录
LOG_HOME = "/data/logs"

# 代码中异常发生时，发送邮件配置
HOSTNAME = socket.gethostname()
ALARM_EMAIL_OPEN = False
ALARM_EMAIL_CONSIGNEE = []

# 开发、测试、灰度、生产
if not hasattr(options, "runmode"):
    define("runmode", default="dev", help="dev gray prod")
    define("debug", default=True, help="enable debug")
    options.parse_command_line()

# 加载相应环境的配置
if options.runmode == "dev":
    from conf.settings_dev import *
elif options.runmode == "test":
    from conf.settings_test import *
elif options.runmode == "gray":
    from conf.settings_gray import *
elif options.runmode == "prod":
    from conf.settings_prod import *
else:
    raise Exception("wrong runmode")
