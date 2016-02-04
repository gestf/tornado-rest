#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
工具函数
'''
import os
import cgi
import time
import gzip
import json
import urllib
import base64
import logging
import urllib2
import StringIO
import urlparse
import datetime
import HTMLParser
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature.PKCS1_v1_5 import PKCS115_SigScheme
from bitarray import bitarray
import decimal


def strptime(str_dtime, time_format='%Y-%m-%d'):
    '''
    字符串转化为 datetime for < 2.6
    @str_dtime: 字符串格式的时间
    @time_format: 时间格式串
    return: datetime.datetime
    '''
    time_stamp = time.mktime(time.strptime(str_dtime, time_format))
    return datetime.datetime.fromtimestamp(time_stamp)

def strftime(dtime, time_format='%Y-%m-%d'):
    '''
    格式化时间
    @dtime: 时间对象
    @time_format: 时间格式串
    return: 字符串时间
    '''
    return datetime.datetime.strftime(dtime, time_format)

def time_start(dtime, dtype):
    '''
    时间取整
    @dtime: datetime.datetime对象
    @dtype: 取整类型 hour day week month
    return: 取整后的时间对象
    '''
    if dtype == 'hour':
        delta = datetime.timedelta(minutes=dtime.minute, seconds=dtime.second,
                                   microseconds=dtime.microsecond)
    elif dtype == 'day':
        delta = datetime.timedelta(hours=dtime.hour, minutes=dtime.minute, seconds=dtime.second,
                                   microseconds=dtime.microsecond)
    elif dtype == 'week':
        delta = datetime.timedelta(days=dtime.weekday(), hours=dtime.hour, minutes=dtime.minute,
                                   seconds=dtime.second, microseconds=dtime.microsecond)
    elif dtype == 'month':
        delta = datetime.timedelta(days=dtime.day-1, hours=dtime.hour, minutes=dtime.minute,
                                   seconds=dtime.second, microseconds=dtime.microsecond)
    else:
        raise Exception('wrong type %s' % dtype)
    return dtime - delta

def time_prev(dtime, dtype):
    '''
    取上一个‘整’时间
    @dtime: datetime.datetime对象
    @dtype: 取整类型 hour day week month
    '''
    dtime = time_start(dtime, dtype)
    return time_start(dtime - datetime.timedelta(seconds=1), dtype)

def time_next(dtime, dtype):
    '''
    取下一个‘整’时间
    @dtime: datetime.datetime对象
    @dtype: 取整类型 hour day week month
    return: 下一个整时间
    '''
    if dtype == 'hour':
        dtime += datetime.timedelta(hours=1)
    elif dtype == 'day':
        dtime += datetime.timedelta(days=1)
    elif dtype == 'week':
        dtime += datetime.timedelta(days=7)
    elif dtype == 'month':
        year = dtime.year + 1 if dtime.month == 12 else dtime.year
        month = 1 if dtime.month == 12 else dtime.month + 1
        dtime = datetime.datetime(year, month, 1)
    else:
        raise Exception('wrong type %s' % dtype)
    return time_start(dtime, dtype)

def time_delta(dtime, days=0, hours=0, seconds=0, time_format='%Y-%m-%d'):
    '''
    给指定时间加上增量
    @dtime: datetime.datetime对象
    @days: 天数
    @hours: 小时
    @seconds: 秒
    return: 加上增量后的时间对象
    '''
    if isinstance(dtime, str):
        dtime = datetime.datetime.strptime(dtime, time_format)
    return dtime + datetime.timedelta(days=days, hours=hours, seconds=seconds)

def time_diff(time1, time2, dtype):
    """
    计算时间差
    :param time1: 起始时间
    :param time2: 结束时间
    :return: 分钟
    """
    date_dict = {
        'second': 1,
        'minite': 60,
        'hour': 60 * 60
    }
    if dtype in date_dict.keys():
        diff = time2 - time1
        actual_sec = diff.days * 24 * 3600 + diff.seconds
        return actual_sec / date_dict.get(dtype, 1)
    else:
        diff = time2 - time1
        return diff.days if diff.days > 0 else 0

def gzip_compress(data):
    '''
    gzip压缩
    @data: 带压缩的数据
    return: 压缩后的数据
    '''
    zbuf = StringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=1, fileobj=zbuf)
    zfile.write(data)
    zfile.close()
    return zbuf.getvalue()

def gzip_decompress(data):
    '''
    gzip解压
    @data: 带解压的数据
    return: 解压后的数据
    '''
    zbuf = StringIO.StringIO(data)
    zfile = gzip.GzipFile(fileobj=zbuf)
    data = zfile.read()
    zfile.close()
    return data

def url_add_params(url, escape=True, **params):
    '''
    往给定url中添加参数
    @url: 给定的URL
    @escape: 是否escape
    @params: 待添加的参数
    return: 添加参数后的url
    '''
    pr = urlparse.urlparse(url)
    query = dict(urlparse.parse_qsl(pr.query))
    query.update(params)
    prlist = list(pr)
    if escape:
        prlist[4] = urllib.urlencode(query)
    else:
        prlist[4] = '&'.join(['%s=%s' % (k, v) for k, v in query.items()])
    return urlparse.ParseResult(*prlist).geturl()

def write2log(basedir, logtype, *row):
    '''
    按天记录日志
    @basedir: 本目录
    @logtype: 日志类型
    @row: 日志内容
    return: None
    '''
    logtype = logtype.lower()
    file_dir = os.path.join(basedir, logtype+'_log')
    os.umask(0)
    if not os.path.lexists(file_dir):
        os.makedirs(file_dir, 0777)
    now = datetime.datetime.now()
    file_name = os.path.join(file_dir, '%s.log' % now.strftime('%Y%m%d'))
    try:
        fd = os.open(file_name, os.O_APPEND|os.O_CREAT|os.O_WRONLY, 0777)
        row = [i.encode('utf8') if isinstance(i, unicode) else str(i) for i in row]
        row.insert(0, now.strftime('[%Y-%m-%d %H:%M:%S]'))
        row = '%s\n' % '\t'.join(row)
        os.write(fd, row)
    except IOError, e:
        logging.error('fail to write %s log: %s\n', logtype, str(e), exc_info=True)
    finally:
        if fd:
            os.close(fd)

def force_utf8(data):
    '''
    数据转换为utf8
    @data: 待转换的数据
    @return: utf8编码
    '''
    if isinstance(data, unicode):
        return data.encode('utf-8')
    elif isinstance(data, list):
        return [force_utf8(i) for i in data]
    elif isinstance(data, dict):
        return {force_utf8(i):force_utf8(data[i]) for i in data}
    return data

def del_dict_key(dict_data, key_list):
    '''
    清空指定键值
    @obj: 清空的字典
    @key_list: 要删除的key列表
    @return: 清理后的dict
    '''
    for key in key_list:
        if key in dict_data:
            del dict_data[key]
    return dict_data

def rsa_sign(private_key, data):
    '''
    生成签名
    @private_key: 私钥
    @data: 待签名数据
    @return: True or False
    '''
    str_data = '&'.join(['%s=%s' % (k, v) for k, v in sorted(data.items()) if k != 'sign' and v != ''])
    h = SHA.new(str_data)
    scheme = PKCS115_SigScheme(RSA.importKey(private_key))
    return base64.b64encode(scheme.sign(h))

def rsa_sign_raw(private_key, str_data):
    '''
    生成签名
    @private_key: 私钥
    @data: 待签名字符串数据
    @return: True or False
    '''
    h = SHA.new(str_data)
    scheme = PKCS115_SigScheme(RSA.importKey(private_key))
    return base64.b64encode(scheme.sign(h))

def rsa_verify(public_key, data):
    '''
    验证签名
    @data: 待验签的数据, 字典形式
    @signature: 签名数据
    @return: True or False
    '''
    str_data = '&'.join(['%s=%s' % (k, v) for k, v in sorted(data.items()) if k != 'sign' and v != ''])
    h = SHA.new(str_data)
    signature = base64.b64decode(data['sign'])
    sign_scheme = PKCS115_SigScheme(RSA.importKey(public_key))
    return sign_scheme.verify(h, signature)

def rsa_verify_raw(public_key, str_data, sign):
    '''
    验证签名
    @data: 待验签的数据, 字符串
    @signature: 签名数据
    @return: True or False
    '''
    h = SHA.new(str_data)
    signature = base64.b64decode(sign)
    sign_scheme = PKCS115_SigScheme(RSA.importKey(public_key))
    return sign_scheme.verify(h, signature)

def escape_html(data):
    '''
    转义html
    '''
    return cgi.escape(data)

def unescape_html(data):
    '''
    反转义html
    '''
    if not isinstance(data, unicode):
        data = data.decode('utf-8')
    parser = HTMLParser.HTMLParser()
    return parser.unescape(data).encode('utf-8')

def convert(num, meta):
    '''
    十进制与其它进制间的转换
    @num: 十进制数字
    @meta: 其它进制e.g: '01'--> 二进制
    '''
    result = ''
    base = len(meta)
    while 1:
        b = num % base
        result = meta[b] + result
        num = num / base
        if num <= 0:
            break
    return result

def json_default(obj):
    '''实现json包对datetime的处理
    '''
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.strftime('%Y-%m-%d %H:%M:%S')

def is_valid_phone(phone):
    '''
    是否是有效的手机号
    '''
    if phone.isdigit() and len(phone) == 11:
        return True
    return False

def send_request(url, params=None, method="GET"):
    '''
    发送请求
    @url: 请求地址
    @params: 请求参数
    return json
    '''
    if params:
        url = '%s?%s' % (url, urllib.urlencode(params))
    if method != "GET":
        url = urllib2.Request(url, urllib.urlencode(params))
    resp = urllib2.urlopen(url)
    res = resp.read()
    resp.close()
    return force_utf8(json.loads(res))

def find_first_zero_postion(binary_str):
    """
    找出一个字符串的二进制格式中，从低位往高位，如果某个位置出现0， 则返回该位置的下标数
    如11011， 第三位为0， 返回下标2。  如果没有0， 则下标位数加1, 返回3
    :param binary_str:
    :return: 位置数编号
    """
    tmp_bit = bitarray()
    tmp_bit.frombytes(binary_str)

    #全是1111的情况下， index(0)方法会报错。 使用try except
    try:
        res = tmp_bit.index(0)
    except:
        res = tmp_bit.length()
    return res

def calculate_page(count, count_per_page):
    """
    根据总数量和每页显示数量，返回总共有多少页
    :param count: 总数量
    :param count_per_page: 每页数量
    :return: 返回总共多少页
    """
    return (count + count_per_page - 1) / count_per_page

def get_id_str(id_list):
    id_list_buffer = set(id_list)
    return ",".join([str(i) for i in id_list_buffer if i])

def get_id_list(obj_list, id_key="id"):
    return [i[id_key] for i in obj_list]

def get_id_str_bylist(obj_list, id_key="id"):
    id_list = [i[id_key] for i in obj_list]
    return get_id_str(id_list)

def fen2yuan(amount):
    """
    转换金额分成元
    :param amount: 转换金额
    :return float: 元
    """
    return float(amount) / 100


def convert_fen_to_yuan(fen):
    """
    转换分到元, 保留两位小数
    
    :param int fen.

    :return str. e.g 1.99
    """

    fen = decimal.Decimal(str(fen))

    a = fen / decimal.Decimal('100')
    return '%0.2f' % a   # end def convert_fen_to_yuan
