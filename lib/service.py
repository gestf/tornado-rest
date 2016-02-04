#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据通用提供服务配置处理器
"""


class ServiceConfig(object):
    """
    数据通用提供服务配置处理器
    """
    @staticmethod
    def get_module_name(module):
        """
        获取当前接口子模块名称
        """
        module_list = module.__module__.split(".")
        if not module_list:
            return None

        return module_list[-1]

    @staticmethod
    def get_handle_service(module, container):
        """
        获取当前接口数据处理服务
        """
        module_name = ServiceConfig.get_module_name(module)
        if not module_name:
            return None

        return container.get(module_name, None)

    @staticmethod
    def get_handle_model(module, container):
        """
        获取当前接口数据处理服务
        """
        module_name = ServiceConfig.get_module_name(module)
        if not module_name:
            return None

        return container.get(module_name, None)

    @staticmethod
    def get_method_params(module, param_config):
        """
        获取子模块方法参数列表
        """
        module_name = ServiceConfig.get_module_name(module)
        if not module_name:
            return None

        return param_config.get(module_name, None)
