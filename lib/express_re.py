#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快递单号正则表达式
"""
import re


def match(express_id, order_no):
    """
    1、韵达快递单号规则：/^\d{13}$/。规则来自韵达官网。
    2、圆通快递单号规则：  /^[A-Za-z0-9]{10,12}$/或/^88[A-Za-z0-9]{16}$/。规则来自圆通官网。
    3、顺丰快递单号运单号只能为12位数字。规则来自顺丰官网。
    4、EMS官网提示编号为13位字符。规则来自EMS官网，EMS官网运单查询只允许查询13位字符。
    5、申通快递单号一般由12或13位数字编码组成。申通官网无规则校验。12位数字在申通官网有说明。13位数字是从管理后台提取的有效快递单号。
    6、天天快递单号一般是由12位字符。规则来自天天官网，天天官网运单查询只允许查询12位字符。
    7、全峰快递单号一般由12位数字和字母组成。全峰官网对运单号只做了数字和字母校验，未做长度校验。管理后台出现了10位和14位编码，但是抽查这部分编码，10位编码为宅急送，14位为快捷速递快递公司。
    8、德邦快递单号一般由8到10位数字编码组成。规则来自德邦官网。
    9、汇通快递单号规则：/[A-Z]\d{10,12}|[A-Z]{2}\d{9,11}|[A-Z]{3}\d{8,10}|[A-Z]{4}\d{7,9}|\d{11,14}/ig。规则来自百世汇通官网。
    10、宅急送快递单号国内运单由10位字符组成，国际快递当前无规则。规则来自宅急送官网。管理后台宅急送存在8位数字，但是这部分快递单号在快递100无记录。
    11、国通的快递单号规则不确定，国通官网位对快递单号未做任何规则校验。管理后台国通单据存在10、12、15位，但是12和15位运单号抽查在国通官网查询无记录。
    12、中通单号规则：国内运单由12位字符组成。国际单号无规则校验。规则来自中通官网。
    13、优速单号规则不少于11位数字。规则来自于管理后台数据整理。优速官网没有对运单号做规则校验。
    14、每日优鲜由14位数字组成。规则来自于管理后台
    :param express_id: 快递公司
    :param order_no: 订单号
    :return:
    """
    express_expression = {
        1: "^\d{13}$",
        2: "^([A-Za-z0-9]{10,12}|88[A-Za-z0-9]{16})$",
        3: "^\d{12}$",
        4: "^[A-Za-z0-9]{13}$",
        5: "^\d{12,13}$",
        6: "^[A-Za-z0-9]{12}$",
        7: "^([A-Za-z0-9]{12}|[A-Za-z0-9]{10}|[A-Za-z0-9]{14})$",
        8: "^\d{8,10}$",
        9: "^([A-Z]\d{10,12}|[A-Z]{2}\d{9,11}|[A-Z]{3}\d{8,10}|[A-Z]{4}\d{7,9}|\d{11,14})$",
        10: "^(\d{10}|\d{8})$",
        11: "^(\d{10}|\d{12}|\d{15})$",
        12: "^[A-Za-z0-9]{12}$",
        13: "^\d{11}\d*$",
        14: "^\d{14}$",
    }
    return True if re.match(express_expression[int(express_id)], order_no) else False


if __name__ == "__main__":
    assert match(1, "1"*13)
    assert not match(1, "1"*12)
    assert match(2, "A" * 11)
    assert match(2, "1"* 11)
    assert match(2, "88" + "1"*16)
    assert not match(3, "1"*11)
    assert match(3, "1"*12)
    assert match(4, "1"*13)
    assert match(4, "a"*13)
    assert not match(4, "a"*12)
    assert match(5, "1" * 12)
    assert match(5, "1" * 13)
    assert not match(5, "a" * 13)
    assert match(6, "a" * 12)
    assert match(7, "a"*12)
    assert match(7, "0"*10)
    assert match(7, "0"*14)
    assert not match(7, "0"*11)
    assert match(8, "1" * 8)
    assert match(8, "1" * 10)
    assert not match(8, "1" * 11)
    assert match(10, "1"*10)
    assert match(10, "1"*8)
    assert match(11, "1"*10)
    assert match(11, "1"*12)
    assert match(11, "1"*15)
    assert match(12, "1"*12)
    assert match(12, "a"*12)
    assert not match(13, "a"*12)
    assert match(13, "1"*11)
    assert match(13, "1"*12)
    assert match(13, "1"*100)
    assert match(14, "1"*14)
    assert not match(14, "a"*14)
    assert not match(14, "1"*15)