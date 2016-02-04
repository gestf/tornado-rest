# coding=utf-8

import sys
import datetime
import base64
try:
    import cPickle as pickle
except:
    import pickle


class Migrate(object): 
    
    def __init__(self):
        self.query_list = []

    def add_query(self, query):
        ''' 判断类型是对象还是字符串'''
        if isinstance(query, list):
            self.query_list.extend(query)
        else:
            self.query_list.append(query)
        self.query_list = list(set(self.query_list))

    def export_query(self, fl):
        '''导出部分
        :param fl: 导出数据到文件fl,
        ''' 
        with open(fl, 'a') as f:
            for query in self.query_list:
                # 模块名和类名
                module = query.__module__
                model = str(query).split()[0]

                # 修改id
                _data = query._data
                _data['id'] = str(_data['id'])
                wrapper = {'module': module, 'models': model, 'data': _data}
                serializer  = base64.b64encode(pickle.dumps(wrapper, -1))
                f.write(serializer)
                f.write('\n')

    def import_query(self, fl, override=False):
        '''导入部分
        :param fl: 需要导入的文件，
        :param override: 是否覆盖相同的id数据，默认False
        '''
        with open(fl, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break

                wrapper = pickle.loads(base64.b64decode(line))

                _module = wrapper['module']
                _model = wrapper['models']
                _data = wrapper['data']

                # 判断模块是否加载
                if _module not in sys.modules:
                    __import__(_module)
                module = sys.modules[_module]
                model = getattr(module, _model)
                
                # 是否覆盖
                if override:
                    obj = model(**_data)
                    obj.save()
                else:
                    _id = _data['id']
                    objs = model.objects(id__exists=_id)
                    if not objs:
                        obj = model(**_data)
                        obj.save()
