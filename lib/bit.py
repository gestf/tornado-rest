#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
摘要: 位操作逻辑
"""
import struct


class Bit(object):
    """
    位操作
    """
    @staticmethod
    def set_bit(status, pos):
        """
        置位, 将status指定位置处置为1, pos的下标是已0开始的
        :param status: 状态
        :param pos: 位存储的位置
        :return: status
        """
        status |= 1 << pos
        return status

    @staticmethod
    def get_bit(status, pos):
        """
        取status, pos位置的位
        :param status: 状态
        :param pos:下标从0开始
        :return: 0 or 1
        """
        return status >> pos & 1

    @staticmethod
    def clear_bit(status, pos):
        """
        清空指定位置的位
        :param status:状态值
        :param pos:位置
        :return status
        """
        status &= ~(1 << pos)
        return status

    @staticmethod
    def is_full(status, size):
        """
        判断status的低size位是否全为一
        :param status:状态值
        :param size:位的个数
        :return: True or False
        """
        value = 2**size - 1
        return status&value == value

    @staticmethod
    def count_bit(status):
        """
        统计status里面1的个数
        :param status: 状态值
        :return: 1的个数
        """
        cnt = 0
        while status:
            status &= status - 1
            cnt += 1
        return cnt

    @staticmethod
    def set_binary_bit(binary, pos):
        """
        置位, 将status指定位置处置为1, pos的下标是已0开始的
        :param status: 任务状态
        :param pos: 位存储的位置
        :return: binary
        """
        length = len(binary) * 8
        if pos >= length:
            binary += "\x00" * ((pos - length) / 8 + 1)
        idx, offset = pos / 8, pos % 8
        slot = struct.unpack("B", binary[idx])[0] | 1 << offset
        return binary[:idx] + struct.pack("B", slot) + binary[idx+1:]

    @staticmethod
    def get_binary_bit(binary, pos):
        """
        取status, pos位置的位
        :param binary: 二进制字符串
        :param pos:位的索引
        :return: 0 or 1
        """
        length = len(binary) * 8
        if pos >= length:
            return 0
        idx, offset = pos / 8, pos % 8
        slot = struct.unpack("B", binary[idx])[0]
        return slot >> offset & 1

    @staticmethod
    def count_binary_bit(binary):
        """
        计数为1的位数
        :param binary: 二进制字符串
        :return: 为1的位数
        """
        count = 0
        for i in binary:
            byte = struct.unpack("B", i)[0]
            count += Bit.count_bit(byte)
        return count

