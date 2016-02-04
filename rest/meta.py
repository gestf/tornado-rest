#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
rest meta class function
"""


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
            if hasattr(item, "_route_rule"):
                if item._route_rule.get("default"):
                    cls._default_item = item
                else:
                    rule_list = parse_rule_list(item._route_rule)
                    if rule_list:
                        cls._route_rules.append((item, rule_list))

        return super(RestMetaclass, cls).__init__(name, bases, attrs)
