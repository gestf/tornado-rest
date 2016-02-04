#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
支付宝
"""
import json
import urllib
import hashlib
import urllib2
import urlparse
import datetime
from xml.etree import ElementTree


class AlipayQRCodeClient(object):
    """
    支付宝扫码支付
    """
    def __init__(self, conf):
        """
        初始化配置
        @conf:{
            "partner":"合作者身份ID",
            "gateway":"支付宝请求网关",
            "notify_url":"服务器异步通知URL",
            "return_url":"前端同步通知URL",
            "ali_secret":"支付宝秘钥"
        }
        """
        self.conf = conf

    def request_qrcode(self, subject, total_fee, **kargs):
        """
        请求生成二维码
        :param subject: 商品描述
        :param total_fee: 充值金额
        :param kargs: 扩展信息
        :return: True or False, {
            "qrcode":"二维码",
            "qrcode_img_url":"二维码图像地址"
            "result_code":"SUCCESS"
            "error_message":"错误信息"
        }
        """
        url, data = self.gen_qrcode_request(subject, total_fee)
        resp = urllib2.urlopen(url, data, timeout=5).read()
        result = self.parse_xml_data(resp)
        if result["is_success"] != "T":
            return False, None
        if result["response"]["alipay"]["result_code"] == "SUCCESS":
            return True, result["response"]["alipay"]
        else:
            return False, result["response"]["alipay"]

    def parse_xml_data(self, text):
        """
        解析返回的XML结果
        """
        if text.find('<?xml version="1.0" encoding="GBK"?>') >= 0:
            text = text.replace('<?xml version="1.0" encoding="GBK"?>',
                                '<?xml version="1.0" encoding="UTF-8"?>')
            text = text.decode("gbk").encode("utf-8")
        root = ElementTree.fromstring(text)
        return self._parse_xml(root)

    def _parse_xml(self, node):
        """
        递归解析xml
        """
        result = {}
        for i in node.getchildren():
            if i.getchildren():
                result[i.tag] = self._parse_xml(i)
            else:
                result[i.tag] = i.text
        return result

    def gen_qrcode_request(self, subject, total_fee):
        """
        生成扫码支付交易请求URL 和 参数
        @total_fee: 商品价格, 单位: RMB－分
        return: 经过签名的移动扫码支付请求URL
        """
        biz_data = {
            "trade_type": "1",  # 即时到帐
            "need_address": "F",
            "goods_info":{
                "id":"10000",
                "name":subject,
                "price":"%s" % (float(total_fee)/100),
            },
            "return_url":self.conf["qrcode"]["return_url"],
            "notify_url":self.conf["qrcode"]["notify_url"],
        }
        param = {
            "service": "alipay.mobile.qrcode.manage",
            "_input_charset": "utf-8",
            "sign_type": "MD5",
            "partner": self.conf["partner"],
            "timestamp":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "method": "add",
            "biz_type": "10",
            "biz_data": json.dumps(biz_data),
        }
        param["sign"] = self.build_signature(param)
        return self.conf["gateway"], urllib.urlencode(param)

    def verify_release(self, post_data):
        """
        验证支付宝下单请求
        @post_data: 下单请求数据
        return: True or False
        """
        data = dict(urlparse.parse_qsl(post_data))

        # TODO: 签名验证
        return True, data

    def verify_notify_data(self, post_data):
        """
        验证支付宝扫码支付后的异步通知
        @post_data: 下单请求数据
        return: True or False
        """
        # TODO: 签名验证
        post_data = dict(urlparse.parse_qsl(post_data))
        data = self.parse_xml_data(post_data["notify_data"])

        # 把元转化为分
        data["total_fee"] = int(float(data["total_fee"]) * 100)

        return True, data

    def is_trade_succ(self, data):
        """
        判断交易是否成功
        """
        if data["trade_status"] not in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            return False
        else:
            return True

    def build_signature(self, param):
        """
        构造签名
        """
        param = self.filter_param(param)
        temp, param_keys = "", param.keys()
        for k in sorted(param_keys):
            temp += "%s=%s&" % (k, param[k])
        temp = "%s%s" % (temp[:-1], self.conf["ali_secret"])
        return hashlib.md5(temp).hexdigest()

    @staticmethod
    def filter_param(param):
        """
        过滤参数
        """
        result = {}
        for k in param:
            if param[k] and k not in ("sign", "sign_type"):
                result[k] = param[k]
        return result

