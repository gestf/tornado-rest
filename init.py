#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动服务
"""
# sys
import os
import sys
import logging

# tornado
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options

define("port", default=8423, help="run on this port", type=int)
define("debug", default=True, help="enable debug mode")
define("runmode", default="dev", help="dev gray prod")
define("project_path", default=sys.path[0], help="deploy_path")

tornado.options.parse_command_line()

if options.debug:
    import tornado.autoreload

# API处理器
from models.profile import Profile
from handler.profile import ProfileHandler
from rest.route import routes, rest_routes


class Application(tornado.web.Application):
    """
    应用类
    """

    def __init__(self):
        """
        应用初始化
        """
        settings = {
            "xsrf_cookies": False,
            "site_title": "demo",
            "debug": options.debug,
            "runmode": options.runmode,
            "template_path": os.path.join(options.project_path, "tpl"),
            "static_path": os.path.join(options.project_path, "static"),
        }
        handlers = [
            rest_routes(Profile, ProfileHandler),
        ]
        tornado.web.Application.__init__(self, routes(handlers), **settings)

    def log_request(self, handler):
        """
        定制如何记录日志
        @handler: request handler
        """
        status = handler.get_status()
        if status < 400:
            log_method = logging.info
        elif status < 500:
            log_method = logging.warning
        else:
            log_method = logging.error
        request_time = 1000.0 * handler.request.request_time()
        if request_time > 30.0 or options.debug or status >= 400:
            log_method("%s %d %s %.2fms", options.port, status,
                       handler._request_summary(), request_time)

if __name__ == "__main__":
    logging.info('listen port: %s', options.port)
    tornado.httpserver.HTTPServer(Application(), xheaders=True).listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
