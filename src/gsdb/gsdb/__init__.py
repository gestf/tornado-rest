'''
Database related setup and hacks.
'''
from auxiliary import random_select,\
                      random_select_multi,\
                      document_iter,\
                      change_lut_on_save
from switch_rp import switch_rp

__all__ = ['random_select',
           'random_select_multi',
           'document_iter',
           'change_lut_on_save',
           'switch_rp']

__VERSION__ = '0.1.2'
