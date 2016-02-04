# -*- coding=utf-8 -*-
"""
base rest class
"""
import gsweb
from gsweb.rest import route
from tornado.web import RequestHandler

import conf.status_code as sc


class Restful(RequestHandler):
    """
    base rest class
    """
    @classmethod
    def send_result(cls, code, result=None, msg=None):
        """
        return rest result format
        """
        return code, result or {}, msg or sc.ERR_DESC.get(code, "未知")

    @route(default=True)
    def error(self, req):
        """
        error http method request
        """
        print req.path
        return self.send_result(sc.E_FORBIDDEN, msg=u"错误的http方法" + gsweb.get_rest_method(req))
