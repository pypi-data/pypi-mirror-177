# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : PyGameAutoAndroid.py
# Time       ：2022.8.30 23:53
# Author     ：小派精灵
# HomePage   : xiaopy.cn
# Email      : 3383716176@qq.com
# Description：
"""

import time


class xp:
    class Point:
        def __init__(self):
            self.x = None
            self.y = None

    @classmethod
    def tap(cls, x1: float, y1: float, duration: float = 0.05):
        """
        点击
        :param x1: x坐标
        :param y1: y坐标
        :param duration: 持续时间
        :return:
        """
        pass

    @classmethod
    def swipe(cls, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, duration: float = 0.3):
        """
        滑动
        :param x1: 起点 x 坐标
        :param y1: 起点 y 坐标
        :param x2: 终点 x 坐标
        :param y2: 终点 y 坐标
        :param duration: 滑动时间
        :return:
        """
        pass

    @classmethod
    def matchColor(cls, colorDesc: str, x: int = 0, y: int = 0):
        """
        匹配颜色
        :param colorDesc: 颜色描述
        :param x: x 坐标
        :param y: y 坐标
        :return:
        """
        pass

    @classmethod
    def findColor(cls, mainColorDesc: str, multiColorDesc: str, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0):
        """
        多点找色
        :param mainColorDesc: 主点颜色描述
        :param multiColorDesc: 多点颜色描述
        :param x1: 起点 x 坐标
        :param y1: 起点 y 坐标
        :param x2: 终点 x 坐标
        :param y2: 终点 y 坐标
        :return:
        """
        return Point()

    @classmethod
    def findImage(cls, imgName: str, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, sim: float = 0.9):
        """
        找图
        :param imgName: 图片名称, 包含后缀
        :param x1: 起点 x 坐标
        :param y1: 起点 y 坐标
        :param x2: 终点 x 坐标
        :param y2: 终点 y 坐标
        :param sim: 相似度
        :return:
        """
        return Point()

    @classmethod
    def findText(cls, text: str, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, sim: float = 0.9):
        """
        文字查找
        :param text: 文本内容
        :param x1: 起点 x 坐标
        :param y1: 起点 y 坐标
        :param x2: 终点 x 坐标
        :param y2: 终点 y 坐标
        :param sim: 相似度
        :return:
        """
        return Point()

    @classmethod
    def getText(cls, x1: int, y1: int, x2: int, y2: int):
        """
        文字判断
        :param x1: 起点 x 坐标
        :param y1: 起点 y 坐标
        :param x2: 终点 x 坐标
        :param y2: 终点 y 坐标
        :return:
        """
        pass

    @classmethod
    def log(cls, msg: str):
        """
        日志框打印
        :param msg: 日志内容
        :return:
        """
        pass

    @classmethod
    def console(cls, **msg: str):
        """
        真机调试 开发日志打印
        :param msg: 日志内容
        :return:
        """
        pass
