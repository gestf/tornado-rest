#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DataManager(object):
    """
    data manager base define.
    """
    def __init__(self, model):
        """
        init
        :param model: data model
        """
        self.model = model

    def get_dict(self, resource):
        """
        get model json dict.
        :param resource: model resource
        """
        pass

    def get_model_list(self):
        """
        get model data list.
        """
        pass

    def get_model_by_id(self, object_id):
        """
        get model data by object id.
        """
        pass

    def save_model(self, data):
        """
        save model.
        """
        pass

    def update_model(self, model, data):
        """
        update model.
        """
        pass

    def delete_model(self, model):
        """
        delete model.
        """
        pass
