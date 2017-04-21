# -*- encoding:utf8 -*-

import requests
from bs4 import BeautifulSoup as bs
from website import *
import sys
import os
import time
from CONSTANTS import *
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

host = 'www.qu.la'
decodeType = 'gb18030'


def save_img(novel_id, img_url):
    img_end = img_url.split('.')[-1]
    parent_path = sys.path[0]
    folder_path = os.path.join(parent_path, r'static')
    folder_path = os.path.join(folder_path, r'img')
    print(folder_path)
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
    file_path = os.path.join(folder_path, str(novel_id) + '.' + img_end)
    if os.path.exists(file_path):
        return
    try:
        img_res = requests.get(img_url, verify=False)
    except:
        s = requests.session()
        s.keep_alive = False
        img_res = s.get(img_url, verify=False)
    doc = open(file_path, 'wb')
    doc.write(img_res.content)
    doc.flush()
    doc.close()
    time.sleep(1)
    return str(novel_id) + img_end


class Novel:
    def __init__(self, novel_url):
        self.novel_url = novel_url
        response = requests.get(self.novel_url)
        if response.status_code != 200:
            return
        content = response.content
        html_source = content.decode(decodeType)
        self.doc = bs(html_source, "html5lib")
        # 作者
        self.author = self.get_novel_author()
        # 内容介绍
        self.intro = self.get_novel_intro()
        self.img = self.get_novel_img()
        DATABASE_INSTANCE = DB()
        self.novel_id = DATABASE_INSTANCE.get_novel_id(novel_url)

    def get_chapter_list(self):
        '''
        获取当前小说的章节列表
        根据不同的来源选择不同的处理
        :return:
        '''
        if not self.__dict__.has_key('doc'):
            return
        if 'www.qu.la' in self.novel_url:
            return self.get_qu_chapter_list()
        return

    def get_qu_chapter_list(self):
        a_list = self.doc.find_all("a")
        return [item for item in a_list if '.html' in str(item)]

    def get_novel_author(self):
        '''
        获取作者姓名
        根据不同的来源选择不同的处理
        :return:
        '''
        if 'www.qu.la' in self.novel_url:
            return self.get_qu_novel_author()
        return

    def get_qu_novel_author(self):
        child_list = self.doc.find("div", attrs={'id': 'info'})
        a= [child.text for child in child_list.children if '作' in str(child) and '者' in str(child)][0]
        return str(a).split("：")[1]

    def get_novel_intro(self):
        '''
        获取当前小说简介
        根据不同的来源选择不同的处理
        :return:
        '''
        if 'www.qu.la' in self.novel_url:
            return self.get_qu_novel_intro()
        return

    def get_qu_novel_intro(self):
        child_list = self.doc.find("div", attrs={'id': 'intro'})
        a = [child.string for child in child_list.children][1]
        return a

    def get_novel_img(self):
        '''
        获取当前小说图片
        根据不同的来源选择不同的处理
        :return:
        '''
        if self.doc is None:
            return
        if 'www.qu.la' in self.novel_url:
            return self.get_qu_novel_img()
        return

    def get_qu_novel_img(self):
        return self.doc.findAll('img')[1]['src']
