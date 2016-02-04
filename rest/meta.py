#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
rest meta class function
"""
import functools


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


def parse_rule_list(rule):
    rule_list = []
    for k, v in rule.items():
        if "__" in k:
            (key, op) = k.split("__", 1)
            rule_list.append((key, op, v))
        else:
            rule_list.append((k, "==", v))
    return rule_list


def match_rule(req, rule_list):
    for (k, op, v) in rule_list:
        attr = getattr(req, k, None)
        if op == "==":
            if attr != v:
                break
        else:
            if not hasattr(attr, op):
                break
            else:
                if not getattr(attr, op)(v):
                    break
    else:
        return True
    return False


class RestMetaclass(type):
    def __init__(cls, name, bases, attrs):
        cls._route_rules = []
        for name in dir(cls):
            item = getattr(cls, name)
            if not (hasattr(item, "_route_rule") and item._route_rule):
                continue

            if item._route_rule.get("default"):
                cls._default_item = item
            else:
                rule_list = parse_rule_list(item._route_rule)
                cls._route_rules.append((item, rule_list))

        return super(RestMetaclass, cls).__init__(name, bases, attrs)
