# -*- encoding:utf8 -*-

import requests
# from bs4 import BeautifulSoup as bs
# from website import *
from novel import *
from chapter import *
import os
import sys,time
reload(sys)
sys.setdefaultencoding("utf-8")

host = 'www.qu.la'
decodeType = 'GB18030'


def website():
    pass

if __name__ == '__main__':
    # 根据小说网站获取小说url 和名称列表
    novel_list = get_novel_list('http://www.qu.la')
    for novel in novel_list:
        # 拼接小说url
        novel_url = 'http://'+host + novel['href']
        novel = Novel(novel_url)
        if novel is None:
            continue
        # 输出小说作者
        print novel.author
        # 输出小说介绍
        print novel.intro
        # 获取最新章节对象
        latest_chapter = novel.get_chapter_list()[0]
        # 获取最新章节url
        latest_chapter_url = novel_url + latest_chapter['href']
        # 获取最新章节名称
        latest_chapter_name = latest_chapter.text
        # 获取全部章节
        chapter_list = novel.get_chapter_list()[1:]
        # # 遍历列表
        for item in chapter_list:
            if item is None:
                continue
            # 获取章节url
            chapter_url = novel_url + item['href']
            # 获取章节名称
            chapter_name = item.text
            print chapter_url
            # print chapter_name
            chapter = Chapter(chapter_url)
            # 输出当前章节内容
            print chapter.content
            # 输出前一章URL
            print chapter.get_previous_chapter()
            # 输出下一章URL
            print chapter.get_next_chapter()
            print '---------------------------------'
            break
        break






