'''
Provide a mechanism for switch the context of read_preference
for mongoengine.

Use patch_BaseQuerySet() once in your file, then you may use
switch_rp() or switch_read_preference() to switch you context.

Example
-------
with switch_rp("PRIMARY"):
    # mongoengine queries
'''
import types
from threading import local
from pymongo.read_preferences import ReadPreference
from engine.queryset.base import BaseQuerySet


class ReadPreferenceLocal(local):
    '''
    threading.local storage of read preference.
    '''
    def __init__(self, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value

read_preference_local = ReadPreferenceLocal(None)


def patch_BaseQuerySet():
    if not hasattr(BaseQuerySet.__init__.im_func, '__patched'):
        origin_init = BaseQuerySet.__init__

        def new_init(self, *sub, **kw):
            origin_init(self, *sub, **kw)
            self._read_preference = read_preference_local.value
        BaseQuerySet.__init__ = new_init
        setattr(BaseQuerySet.__init__.im_func, '__patched', True)


class switch_read_preference(object):
    def __init__(self, preference, tag_sets_disabled=False):
        '''
        preference could be ReadPreference's attributes:
            ReadPreference.NEAREST
            ReadPreference.PRIMARY
            ReadPreference.PRIMARY_PREFERRED
            ReadPreference.SECONDARY
            ReadPreference.SECONDARY_ONLY
            ReadPreference.SECONDARY_PREFERRED
        or simply one of the following strings:
            'NEAREST', 'PRIMARY', 'PRIMARY_PREFERRED', 'SECONDARY',
            'SECONDARY_ONLY', 'SECONDARY_PREFERRED'
        '''
        if isinstance(preference,
                      (types.IntType, types.LongType, types.NoneType)):
            self._preference = preference
        else:
            self._preference = getattr(ReadPreference, preference)

        # ReadPreference.PRIMARY could not be used with tag_sets
        if not tag_sets_disabled and self._preference == ReadPreference.PRIMARY:
            self._preference = ReadPreference.PRIMARY_PREFERRED

        self._original = None

    def __enter__(self):
        self._original = read_preference_local.value
        read_preference_local.value = self._preference

    def __exit__(self, exc_type, exc_value, traceback):
        read_preference_local.value = self._original
        if exc_type:
            raise exc_type, exc_value, traceback

switch_rp = switch_read_preference

patch_BaseQuerySet()
