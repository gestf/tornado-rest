#-*-coding:utf-8 -*-
import time
import datetime
import calendar


def to_local_format(time):
    return time.strftime(u'%Y年%m月%d日 %H:%M:%S')


def increase_day(day, source=None):
    '''
    根据给定的source date, 获得增加一定天数的时间
    '''
    source = source if source else datetime.datetime.now()
    return source + datetime.timedelta(days=day)


def increase_month(month, source=None):
    '''
    根据给定的source date, 获得增加一定月份的时间
    '''
    source = source if source else datetime.datetime.now()
    _m = source.month - 1 + month
    _y = source.year + _m / 12
    _m = _m % 12 + 1
    _d = min(source.day, calendar.monthrange(_y, _m)[1])
    return type(source)(_y, _m, _d)


def increase_year(year, source=None):
    '''
    根据给定的source date, 获得增加一定天数的时间
    '''
    source = source if source else datetime.datetime.now()
    _y = source.year + year
    _m = source.month
    _d = min(source.day, calendar.monthrange(_y, source.month)[1])
    return type(source)(_y, _m, _d)


def increase_hour(hour, source=None):
    '''
    根据给定的source date, 获得增加一定小时的时间
    '''
    source = source if source else datetime.datetime.now()
    return source + datetime.timedelta(hours=hour)


def increase_period(period, source=None):
    '''
    根据给定的source date, 获得增加一定月份的时间
    '''
    if not period:
        return source

    if period.endswith('y'):
        _year = int(period.split('y')[0])
        return increase_year(_year, source)
    elif period.endswith('m'):
        _month = int(period.split('m')[0])
        return increase_month(_month, source)
    elif period.endswith('d'):
        _day = int(period.split('d')[0])
        return increase_day(_day, source)
    elif period.endswith('h'):
        _h = int(period.split('h')[0])
        return increase_hour(_h, source)
    else:
        return source


def format_seconds(sec):
    '''
    Convert seconds to "HH:MM:SS" format representation.
    '''
    sec = int(sec)
    hours = sec / 3600
    minutes = sec % 3600 / 60
    seconds = sec % 60
    return '%02d:%02d:%02d' % (hours, minutes, seconds)


def utc_to_local(utc_dt):
    '''
    Convert utc datetime object to local datetime object.
    '''
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    return local_dt


def utc_to_timestamp(utc_dt):
    timestamp = calendar.timegm(utc_dt.timetuple())
    return timestamp


def format_timestamp(ts, scale=1000, date_format='%Y-%m-%d %H:%M:%S'):
    '''
    format_timestamp(ts, scale=1000, date_format='%Y-%m-%d %H:%M:%S')
    Convert a timestamp(default in milliseconds) to a datetime format.
    '''
    return datetime.datetime.fromtimestamp(ts / scale).strftime(date_format)


def strptime(str_dtime, time_format='%Y-%m-%d %H:%M:%S'):
    '''
    字符串转化为 datetime for < 2.6
    @str_dtime: 字符串格式的时间
    @time_format: 时间格式串
    return: datetime.datetime
    '''
    time_stamp = time.mktime(time.strptime(str_dtime, time_format))
    return datetime.datetime.fromtimestamp(time_stamp)


def strftime(dtime, time_format='%Y-%m-%d %H:%M:%S'):
    '''
    格式化时间
    @dtime: 时间对象
    @time_format: 时间格式串
    return: 字符串时间
    '''
    return datetime.datetime.strftime(dtime, time_format)


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
