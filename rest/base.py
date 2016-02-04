#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handler基类
"""
import json
import logging
import functools

import tornado.web
from tornado.options import options

from lib.debug import get_debug_context
from lib.mail import Mail
from lib.utils import json_default, write2log
from conf.settings import (LOG_HOME, HOSTNAME, ALARM_EMAIL_OPEN,
                           ALARM_EMAIL_SEND_NAME, ALARM_EMAIL_SEND_PWD,
                           ALARM_EMAIL_CONSIGNEE)
from conf.status_code import (ERR_DESC, E_SUCC, E_INTER, E_PARAM,
                              E_FORBIDDEN, E_RESOURCE_NOT_FIND)
from rest.meta import match_rule


class ParamException(Exception):
    """
    param exception.
    """
    code = E_PARAM
    msg = None

    def __init__(self, msg, *args, **kwargs):
        super(ParamException, self).__init__(*args, **kwargs)
        self.msg = msg


def route(**rule):
    """
    Decorator indicating the routes for current view.
    """
    def entangle(func):
        @functools.wraps(func)
        def wrapper(self, *sub, **kw):
            ret = func(self, *sub, **kw)
            return ret
        wrapper._route_rule = rule
        return wrapper
    return entangle


class BaseHandler(tornado.web.RequestHandler):
    """
    base request handler, responsible for dispatch request function.
    """
    ARG_DEFAULT = object()

    def render_error_html(self):
        """
        generate error html page.
        """
        if ALARM_EMAIL_OPEN:
            context = get_debug_context()
            if context:
                context["arguments"] = self.request.arguments
                return self.render_string("error.html",
                                          **context)
        return ""

    def alarm_exception(self, html, error=None):
        """
        responsible for send alarm html email.
        :param html: html page string,
        :param error: error info.
        """
        if ALARM_EMAIL_OPEN and html:
            logging.error("send error report mail")
            mail = Mail("smtp.qq.com", ALARM_EMAIL_SEND_NAME, ALARM_EMAIL_SEND_PWD)
            subject = HOSTNAME + ": " + repr(error) if error else "代码异常"
            mail.send(subject,
                      html,
                      ALARM_EMAIL_CONSIGNEE,
                      plugins=[{"subject": "%s.html" % (error.__class__.__name__
                                                        if error else "error"),
                                "content": html}])

    def send_result(self, code, result=None, msg=None):
        """
        send json standard result data.
        :param code: return code
        :param result: return result
        :param msg: return message
        """
        response = {
            "code": code,
            "msg": msg or ERR_DESC.get(code, "未知"),
            "result": result or {}
        }
        if options.debug:
            logging.info("request: %s", self.request.arguments or self.request.body)
            logging.info("response: %s", json.dumps(response, default=json_default))

        self.finish(response)

    def get_argument(self, name, default=tornado.web.RequestHandler._ARG_DEFAULT,
                     strip=True):
        """
        get string argument.
        """
        value = super(BaseHandler, self).get_argument(name, default, strip)
        if isinstance(value, unicode):
            value = value.encode("utf-8")
        return value

    def get_argument_int(self, name, default=ARG_DEFAULT):
        """
        get int argument.
        :param name: param name
        :param default: default value
        """
        value = self.get_argument(name, default)
        if value == self.ARG_DEFAULT:
            raise ParamException("参数: %s 不能为空" % name)
        elif value == default:
            return value
        try:
            value = int(value)
        except:
            if default != self.ARG_DEFAULT:
                return default
            raise ParamException("参数: %s 格式不正确" % name)
        return value

    def get_argument_float(self, name, default=ARG_DEFAULT):
        """
        get float argument.
        :param name: param name
        :param default: default value
        """
        value = self.get_argument(name, default)
        if value == self.ARG_DEFAULT:
            raise ParamException("参数: %s 不能为空" % name)
        elif value == default:
            return value
        try:
            value = float(value)
        except ValueError:
            if default != self.ARG_DEFAULT:
                return default
            raise ParamException("参数: %s 格式不正确" % name)
        return value

    def get_json_data(self):
        """
        get request body json data.
        """
        json_body = getattr(self.request, '__json_body', None)
        if json_body is None:
            json_body = json.loads(self.request.body) if self.request else {}
            self.request.__json_body = json_body
        return self.request.__json_body

    def get_json_argument(self, name, default=None):
        """
        get request body argument.
        :param name: param name
        :param default: default value
        """
        json_body = self.get_json_data()
        return json_body.get(name, default)

    def process_module(self, *module, **kwargs):
        """
        module unify process function
        :param module: module name
        :param kwargs: expend params
        """
        module = module[0] if module else "default"
        module = '__'.join([i for i in module.split('/') if i])
        self.request.module = module
        for (route_func, rule_list) in self._route_rules:
            if match_rule(self.request, rule_list):
                try:
                    route_func(self, **kwargs)
                except ParamException as ex:
                    logging.error("%s\n%s\n", self.request, str(ex), exc_info=True)
                    return self.send_result(E_PARAM, msg=ex.msg)
                except Exception as ex:
                    message = str(ex)
                    html = self.render_error_html()
                    if isinstance(ex, TypeError):
                        message = "missing or surplus params"
                    logging.error("%s\n%s\n", self.request, message, exc_info=True)
                    self.send_result(E_INTER, msg=message)
                    self.alarm_exception(html, error=ex)
                    return
        else:
            if hasattr(self, "_default_item"):
                return self._default_item(**kwargs)
        raise tornado.web.HTTPError(404)

    def get(self, *module, **kwargs):
        """
        HTTP GET
        """
        self.process_module(*module, **kwargs)

    def post(self, *module, **kwargs):
        """
        HTTP POST
        """
        self.process_module(*module, **kwargs)

    def put(self, *module, **kwargs):
        """
        HTTP PUT
        """
        self.process_module(*module, **kwargs)

    def delete(self, *module, **kwargs):
        """
        HTTP DELETE
        """
        self.process_module(*module, **kwargs)


class RestHandler(BaseHandler):
    """
    rest request handler, responsible for common resource handle.
    """
    @route(method="GET", module="default")
    def get_resource(self, resource_id=None):
        """
        get resource single data or list data.
        :param resource_id: resource id
        """
        try:
            code, result = E_SUCC, {}
            if resource_id:
                model = self.model_engine.get_model_by_id(resource_id)
                if model:
                    result = self.model_engine.get_dict(model)
                else:
                    code = E_RESOURCE_NOT_FIND
            else:
                model_list = self.model_engine.get_model_list()
                result = [self.model_engine.get_dict(i) for i in model_list]

            self.send_result(code, result)
        except Exception as ex:
            self.send_result(E_PARAM, msg=str(ex))

    @route(method="POST", module="default")
    def save_resource(self):
        """
        save resource data
        """
        data = self.get_json_data()
        print data
        try:
            model = self.model_engine.save_model(data)
            self.send_result(E_SUCC, self.model_engine.get_dict(model))
        except Exception as ex:
            self.send_result(E_PARAM, msg=str(ex))

    @route(method="PUT", module="default")
    def update_resource(self, resource_id):
        """
        update resource data
        :param resource_id: resource id
        """
        data = self.get_json_data()
        print data
        try:
            code, resource = E_SUCC, {}
            model = self.model_engine.get_model_by_id(resource_id)
            if model:
                model = self.model_engine.update_model(model, data)
                resource = self.model_engine.get_dict(model)
            else:
                code = E_RESOURCE_NOT_FIND

            self.send_result(code, resource)
        except Exception as ex:
            self.send_result(E_PARAM, msg=str(ex))

    @route(method="DELETE", module="default")
    def delete_resource(self, resource_id):
        """
        delete resource data
        :param resource_id: resource id
        """
        try:
            code, result = E_SUCC, {}
            model = self.model_engine.get_model_by_id(resource_id)
            if model:
                self.model_engine.delete_model(model)
                result = {"resource_id": resource_id}
            else:
                code = E_RESOURCE_NOT_FIND

            self.send_result(code, result)
        except Exception as ex:
            self.send_result(E_PARAM, msg=str(ex))

    @route(default=True)
    def error(self, **kwargs):
        """
        error http method request
        """
        print kwargs
        print self.request.path
        self.send_result(E_FORBIDDEN, msg=u"当前资源不支持%s请求" % self.request.method)
