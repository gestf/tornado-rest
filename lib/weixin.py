#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信
"""
import uuid
import hashlib
import logging
import StringIO
from lib.httpclient import HttpClient
from xml.etree import ElementTree


# 交易类型
TRADE_TYPE_JSAPI = "JSAPI"
TRADE_TYPE_NATIVE = "NATIVE"
TRADE_TYPE_APP = "APP"


def parse_xml_data(text):
    """
    解析XML数据
    :param string text: 待解析的XML文本
    """
    root = ElementTree.fromstring(text)
    data = {}
    for i in root.getchildren():
        data[i.tag] = i.text
    return data


def generate_xml(data):
    """
    生成XML数据
    :param string text: 待解析的XML文本
    """
    root = ElementTree.Element("xml")
    tree = ElementTree.ElementTree(root)
    for i in data:
        child = ElementTree.Element(i)
        if isinstance(data[i], str):
            text = data[i].decode("UTF-8")
        elif isinstance(data[i], unicode):
            text = data[i]
        else:
            text = "%s" % data[i]
        child.text = text
        root.append(child)
    fobj = StringIO.StringIO()
    tree.write(fobj, "UTF-8")
    return fobj.getvalue()


class WeixinPayClient(object):
    """
    微信扫码支付
    """
    def __init__(self, conf):
        """
        初始化配置
        :param dict conf:{
            "appid":"应用ID",
            "key":"长度为32的API KEY",
            "appsecret":"长度为32的字符串",
            "mch_id":"商户号",
            "notify_url":"服务器异步通知URL",
        }
        """
        self.conf = conf
        self.http = HttpClient(timeout=5)
        self.unifiedorder_url = "https://api.mch.weixin.qq.com/pay/unifiedorder"

    def create_prepay(self, trade_type, body, total_fee, out_trade_no):
        """
        创建预支付交易
        :param trade_type: 交易类型
        :param string body: 商品描述
        :param int total_fee: 商品价格, 单位: RMB－分
        :param string out_trade_no: 交易号(在商户系统中唯一)
        :return:{
            "prepayid":"PREPAY_ID",
            "code_url":"二维码链接",
            "return_code":"Success or FAIL",
            "return_msg":"错误原因"
        }
        """
        # 请求参数
        param = {
            "appid": self.conf["appid"],
            "mch_id": self.conf["mch_id"],
            "nonce_str": hashlib.md5(str(uuid.uuid4())).hexdigest(),
            "body": body,
            "out_trade_no": out_trade_no,
            "fee_type": "CNY",
            "total_fee": int(total_fee),
            "spbill_create_ip": "127.0.0.1",         # Native支付填调用微信支付API的机器IP
            "notify_url": self.conf["qrcode"]["notify_url"],
            "trade_type": trade_type,
            "product_id": out_trade_no,
        }
        param["sign"] = self.build_signature(param)

        # 生成XML数据
        xml_text = generate_xml(param)

        # POST请求, 解析XML
        try:
            response = self.http.http_post(self.unifiedorder_url, "text",
                                           body=xml_text)
        except:
            logging.error("fail to request weixin prepay: %s", param)
            return None

        res = parse_xml_data(response)
        if res["return_code"] != "SUCCESS" or res["result_code"] != "SUCCESS":
            logging.error("fail to create prepay: %s, %s", param, res)
            return None

        # 验证签名
        if not self.verify_signature(res):
            logging.error("fail to verify signature: %s", res)
            return None

        info = {
            "prepayid":res["prepay_id"],
            "qrcode":res.get("code_url", ""),
            "qrcode_img_url":""
        }
        return info

    def request_qrcode(self, subject, total_fee, **kargs):
        """
        请求生成二维码
        :param subject: 商品描述
        :param total_fee: 充值金额
        :param kargs: 扩展信息
        :return: False or True, {
            "qrcode":"二维码",
            "qrcode_img_url":"二维码图像地址"
        }
        """
        result = self.create_prepay(TRADE_TYPE_NATIVE, subject, total_fee,
                                    kargs["out_trade_no"])
        return bool(result), result

    def build_signature(self, param):
        """
        构造签名
        """
        temp_str = "&".join(["%s=%s" % (k, v) for k, v in \
                             sorted(param.items()) if str(v) and k != "sign"])
        temp_str += "&key=%s" % self.conf["key"]
        print 'build weixin signature:', temp_str
        return hashlib.md5(temp_str).hexdigest().upper()

    def verify_signature(self, param):
        """
        验证签名
        """
        return param["sign"] == self.build_signature(param)

    def verify_notify_data(self, post_data):
        """
        校验异步通知数据
        :param string post_data: 通知数据
        :return: 是否验证通过, 通知数据(DICT){
            "out_trade_no":"商户订单系统中的订单号",
            "trade_no":"该交易在支付宝系统中的交易流水号",
            "trade_status":"交易状态",
            "trade_id":"通知校验ID",
            "total_fee":"交易金额",
            "buyer_id":"买家支付宝用户号",
            "buyer_email":"买家支付宝账号",
            ...
        }
        """
        data = parse_xml_data(post_data)
        if not self.verify_signature(data):
            logging.error("fail to verify signature: %s", data)
            return False, None

        # 微信的交易ID，和支付宝保持统一
        data["trade_no"] = data["transaction_id"]

        return True, data

    @staticmethod
    def is_trade_succ(_):
        """
        判断交易是否成功
        """
        return True

    @staticmethod
    def gen_notify_response():
        """
        生成notify的响应
        """
        data = {
            "return_code":"SUCCESS",
            "return_msg":"OK",
        }
        return generate_xml(data)

