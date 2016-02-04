#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gsdb
import datetime
from utility.lock import cache_lock
from utility.util import sign_data
from lib.date import strftime
from bson.objectid import ObjectId
from mongoengine.document import Document
from rest.backends.base import DataManager


class ModelEngine(DataManager):
    def get_dict(self, resource):
        """
        get model json dict.
        :param resource: model resource
        """
        if not isinstance(resource, Document):
            raise Exception("not a document resource")

        result = {}
        for key in resource._data._classes.keys()[0]:
            value = getattr(resource, key)
            if isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, datetime.datetime):
                result[key] = strftime(value)
            elif isinstance(value, Document):
                result[key] = self.get_dict(value)
            else:
                result[key] = value

        return result

    def get_model_list(self):
        """
        get model data list.
        """
        return self.model.objects.all()

    def get_model_by_id(self, object_id):
        """
        get model data by object id.
        """
        return self.model().get(id=object_id)

    def save_model(self, data):
        """
        save model.
        """
        with cache_lock("save_model_%s" % sign_data(data)):
            with gsdb.switch_rp("PRIMARY"):
                model = self.model(**data)
                model.save()

                return model

    def update_model(self, model, data):
        """
        update model.
        """
        with cache_lock("update_model_%s" % str(model.id)):
            with gsdb.switch_rp("PRIMARY"):
                for key, value in data.items():
                    if key == "id":
                        continue
                    if hasattr(model, key):
                        setattr(model, key, value)

                model.save()
                return model

    def delete_model(self, model):
        """
        delete model.
        """
        with cache_lock("delete_model_%s" % str(model.id)):
            with gsdb.switch_rp("PRIMARY"):
                model.delete()
