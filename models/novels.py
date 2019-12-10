"""
AUTHOR:   MIAN
DATE:     2019/12/5
DESCRIBE: 对小说文件夹的一些操作
"""
from typing import *
from os import listdir, path

base = "static\\novels\\"


class Novel:
    def __init__(self, name: str):
        self.__name = name
        self.__base = base + name
        with open(self.__base + "\\书籍信息.txt", "r") as fp:
            self.describe = fp.read()
        with open(self.__base + "\\封面.jpg", "rb") as fp:
            self.cover = fp.read()
        addr = self.__base + "\\" + name
        self.books = listdir(addr)

    def books_addr(self) -> List[str]:
        """
返回所有的分卷路径
        :return:
        """
        return [self.__base + "\\" + self.__name + "\\" + s for s in self.books]


class Novels:
    def __init__(self):
        self.__base = base
        self.novels = listdir(self.__base)

    def novel_valid(self, name) -> bool:
        return name in self.novels

    def get_novel(self, name) -> Novel or None:
        if name not in self.novels:
            return None
        else:
            return Novel(name)


novel = Novels()