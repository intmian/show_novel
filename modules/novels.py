# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2019/12/5
DESCRIBE: 对小说文件夹的一些操作
"""
from sortedcontainers import SortedList
from typing import *
from os import listdir, path

base = "static/novels/"


class Novel:
    def __init__(self, name: str):
        self.__name = name
        self.__base = base + name
        with open(self.__base + "/书籍信息.txt", "r") as fp: # linux 此处应添加gb2312的解码
            self.describe = fp.read()
        self.cover = self.__base + "/封面.jpg"
        addr = self.__base + "/" + name
        self.books = listdir(addr)

    def books_addr(self) -> List[str]:
        """
返回所有的分卷路径
        :return:
        """
        return [self.__base + "/" + self.__name + "/" + s for s in self.books]


class Novels:
    def __init__(self):
        self.__base = base
        self.novels = listdir(self.__base)
        self.__rank = SortedList(key=lambda t: -t[1])  # 红黑树

        for no in self.novels:
            self.__rank.add([no, 0])

    def novel_valid(self, name) -> bool:
        return name in self.novels

    def get_novel(self, name) -> Novel or None:
        if name not in self.novels:
            return None
        else:
            return Novel(name)

    def add_rank(self, novel_):
        for i in range(len(self.__rank)):
            if self.__rank[i][0] == novel_:
                n = self.__rank[i][1] + 1
                self.__rank.pop(i)
                self.__rank.add([novel_, n])

    def novels_popular(self):
        return self.__rank[0:16]

    def novels_rank(self):
        return list(self.__rank)[0:100]


novel = Novels()
