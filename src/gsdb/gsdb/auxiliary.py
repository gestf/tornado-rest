'''
Provide some auxiliary functions for easy django Model
and mongoengine Document operations.
'''
import datetime
import random
from engine import Document, ValidationError, Q
from engine.queryset.visitor import QNode
from django.db.models.base import Model


def to_query(filters):
    if filters is None:
        filters = {}
    elif isinstance(filters, QNode):
        return filters
    else:
        return Q(**filters)


def model_get(model, **kw):
    '''
    A wrapper of .objects.get for Django.db.models 
    or mongoengine.Document, ignore the DoesNotExist
    and ValidationError error, but raises other errors.
    '''
    if 'id' in kw and kw['id'] is None:
        return None
    try:
        return model.objects.get(**kw)
    except model.DoesNotExist as e:
        return None
    except ValidationError as e:
        return None
    except model.MultipleObjectsReturned as e:
        args = list(e.args)
        args.append(str(kw))
        e.args = tuple(args)
        raise e


def random_select(document, rnd_column='rnd', hint=None, filters=None):
    '''
    Randomly select a document. Note that the method required
    a indexed float column as the radix of each document.
    Parameters
    ----------
    document: Document sub class,
        the class to select.
    rnd_column: The random column,
        the column name of the radix for random select.
    hint: optional, the hint of mongodb queries,
        if not provieded, will use rnd_column as hint.
    filters:
        The filter expression for mongoengine query.
    '''
    rnd = random.random()
    condition = Q(**{'%s__gt' % rnd_column: rnd}) & to_query(filters)
    hint = hint if hint is not None else [(rnd_column, 1)]
    r = document.objects(condition).hint(hint)\
                .order_by(rnd_column).first()
    if not r:
        condition = Q(**{'%s__lte' % rnd_column: rnd}) & to_query(filters)
        r = document.objects(condition).hint(hint)\
                    .order_by(rnd_column).first()
    return r


def random_select_multi(document, rnd_column='rnd',
                        hint=None, limit=10, filters=None):
    '''
    Randomly select a collection of documents. Note that the
    method required a indexed float column as the radix of each document.
    Parameters
    ----------
    document: Document sub class,
        the class to select.
    rnd_column: The random column,
        the column name of the radix for random select.
    hint: optional, the hint of mongodb queries,
        if not provieded, will use rnd_column as hint.
    limit: int, default 10,
        number of document returned at most.
    filters:
        The filter expression for mongoengine query.
    '''
    rnd = random.random()
    condition = Q(**{'%s__gt' % rnd_column: rnd}) & to_query(filters)
    hint = hint if hint is not None else [(rnd_column, 1)]
    ret = list(document.objects(condition).hint(hint)\
                     .order_by(rnd_column).limit(limit))
    if len(ret) < limit:
        condition = Q(**{'%s__lte' % rnd_column: rnd}) & to_query(filters)
        r = list(document.objects(condition).hint(hint)\
                         .order_by(rnd_column).limit(limit - len(ret)))
        ret.extend(r)
    return ret


def document_iter(document, threshold=None, index_column='id',
                  desc=False, filters=None, limit=None):
    '''
    A helper for cursor based iterating over a Document.
    Parameters
    ----------
    document: The mongoengine Document.
    threshold: A comparable value,
        the threshold for next function call.
    index_column: string, default id,
        the column for ordering.
    desc: boolean,
        is descenting order.
    filters: dict,
        filters for Document.objects(**kw) query.
    limit: int,
        max number of items to return.
    Return
    ------
    A tuple (ret, last).
    ret: list,
        The list of documents.
    last: the threshold to use for next call.
        
    '''
    if filters is None:
        filters = {}
    condition = {}
    if threshold is not None:
        op = 'lt' if desc else 'gt'
        condition['%s__%s' % (index_column, op)] = threshold
    condition.update(filters)
    query = document.objects(**condition)
    query = query.order_by('-%s' % index_column) if desc else query.order_by(index_column)
    if limit is not None:
        query = query.limit(limit)
    ret = list(query)
    last = getattr(ret[-1], index_column) if ret else None
    return ret, last


def change_lut_on_save(document_class):
    '''
    A decorator for Document sub classes.
    If the class have lut field, change it to
    current datetime when save function is called.
    '''
    original_save = document_class.save

    def save_with_lut(self, **kw):
        if hasattr(self, 'lut'):
            self.lut = datetime.datetime.now()
        original_save(self, **kw)

    document_class.save = save_with_lut
    return document_class


print("Patching Model/Document class for .get method")
Model.get = classmethod(model_get)
Document.get = classmethod(model_get)
Document._iter = classmethod(document_iter)
