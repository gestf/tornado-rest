#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf.settings as settings
from rest.base import RestHandler
from importlib import import_module

support_actions = set(("get", "list", "post", "put", "delete"))


def routes(route_list):
    routes = []
    for route in route_list:
        if isinstance(route, list):
            routes.extend(route)
        else:
            routes.append(route)
    return routes


def get_available_actions(**kwargs):
    action = set(kwargs.get("action", []))
    exclude = set(kwargs.get("exclude", []))
    if not action:
        action = support_actions

    return action - exclude


def rest_routes(model, handler=None, **kwargs):
    prefix = kwargs.get("prefix", model.__name__.lower())
    handler = handler or RestHandler
    try:
        engine = import_module(settings.MODEL_ENGINE)
        handler["model_engine"] = engine.ModelEngine(model)
    except AttributeError:
        from rest.backends.mongo import ModelEngine
        handler["model_engine"] = ModelEngine
    active_routes = get_available_actions(**kwargs)

    routes = []
    if active_routes.intersection(set(["post", "list"])):
        route = (r"/api/v1/%s/?" % prefix, handler)
        routes.append(route)

    if active_routes.intersection(set(["get"])):
        route = (r"/api/v1/%s/([a-z_A-Z/]*)/?" % prefix, handler)
        routes.append(route)

    if active_routes.intersection(set(["get", "put", "delete"])):
        route = (r"/api/v1/%s/(?P<resource_id>[^\/]+)" % prefix, handler)
        routes.append(route)

    return routes