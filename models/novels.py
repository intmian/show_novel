"""
AUTHOR:   MIAN
DATE:     2019/12/5
DESCRIBE: 对小说文件夹的一些操作
"""
from typing import *
from os import listdir

class Novel:
    def __init__(self,name:str):
        self.__base = "..\\static\\novels\\" + name
        with open(self.__base + "\\书籍信息.txt","r") as fp:
            self.describe = fp.read()
        with open(self.__base + "\\封面.jpg","r") as fp:
            self.cover = fp.read()


class Novels:
    def __init__(self):
        self.__base = '..\\static\\novels'
        self.novels = listdir(self.__base)

    @staticmethod
    def get_names() -> List[str]:
        """
    获得书目
        :return: 书名列表
        """
        addr = '..\\static\\novels'
        return listdir(addr)

    def get_novel(self,name) -> Novel or None:
        if name not in self.novels:
            return None
        else:
            addr  = self.__base +




