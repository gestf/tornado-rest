#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest.backends.engine import MongoEngineDataManager

dynamic_classes_cache = {}
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


def rest_routes(model, handler, **kwargs):
    handler.data_manager = MongoEngineDataManager(model)
    prefix = kwargs.get("prefix", model.__name__.lower())
    routes = []

    active_routes = get_available_actions(**kwargs)

    if active_routes.intersection(set(["post", "list"])):
        route = (r"/api/v1/%s/?" % prefix, handler)
        routes.append(route)

    if active_routes.intersection(set(['get'])):
        route = (r'/api/v1/%s/([a-z_A-Z/]*)/?' % prefix, handler)
        routes.append(route)

    if active_routes.intersection(set(["get", "put", "delete"])):
        route = (r"/api/v1/%s/(?P<resource_id>[^\/]+)" % prefix, handler)
        routes.append(route)

    return routes