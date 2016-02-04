#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf.settings as settings
from rest.base import RestHandler
from rest.rule import RestMetaclass
from importlib import import_module

support_actions = set(("get", "list", "post", "put", "delete"))


def routes(route_list):
    """
    settle route and handler mapping tuple.
    :param route_list: route handler list
    """
    routes = []
    for route in route_list:
        if isinstance(route, list):
            routes.extend(route)
        else:
            routes.append(route)
    return routes


def get_available_actions(**kwargs):
    """
    get available actions, filter enable request method.
    :param kwargs: extend params.
    """
    action = set(kwargs.get("action", []))
    exclude = set(kwargs.get("exclude", []))
    if not action:
        action = support_actions

    return action - exclude


def rest_routes(model, handler=RestHandler, **kwargs):
    """
    route rest handle.
    :param model: resource model
    :param handler: resource handler
    :param kwargs: action exclude
    :return: route handler tuple
    """
    prefix = kwargs.get("prefix", model.__name__.lower())
    dynamic_attr = {}
    try:
        engine = import_module(settings.MODEL_ENGINE)
    except AttributeError:
        raise Exception("settings missing MODEL_ENGINE config")

    dynamic_attr["model_class"] = model
    dynamic_attr["model_engine"] = engine.ModelEngine(model)
    handler = RestMetaclass(handler.__name__, handler.__bases__,
                            dict(handler.__dict__.items() + dynamic_attr.items()))
    active_routes = get_available_actions(**kwargs)

    route_set = []
    if active_routes.intersection(set(["post", "list"])):
        route = (r"/api/v1/%s/?" % prefix, handler)
        route_set.append(route)

    if active_routes.intersection(set(["get"])):
        route = (r"/api/v1/%s/([a-z_A-Z/]*)/?" % prefix, handler)
        route_set.append(route)

    if active_routes.intersection(set(["get", "put", "delete"])):
        route = (r"/api/v1/%s/(?P<resource_id>[^\/]+)" % prefix, handler)
        route_set.append(route)

    return route_set
