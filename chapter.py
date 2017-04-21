# -*- encoding:utf8 -*-

import requests
from bs4 import BeautifulSoup as bs
from website import *
import sys,os
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

decodeType = 'GB18030'






class Chapter:

    def __init__(self, chapter_url):
        print chapter_url
        self.chapter_url = chapter_url
        self.html_source = self.get_html_by_url()
        if self.html_source is None or "很抱歉，您要访问的页面不存在!" in self.html_source or "reason" in self.html_source:
            self.doc = None
            self.content = None
            self.previous_chapter = None
            self.next_chapter = None
            return
        # self.doc = bs(html_source, "html.parser")
        self.doc = bs(self.html_source, "html5lib")
        # 当前的章节内容
        self.content = self.get_chapter_content()
        # 下一章节的完整url
        self.next_chapter = self.get_next_chapter()
        # 上一章节的完整url
        self.previous_chapter = self.get_previous_chapter()

    def get_html_by_url(self):
        try:
            response = requests.get(self.chapter_url)
        except:
            response = requests.get(self.chapter_url)
        if response.status_code != 200:
            return
        try:
            response.encoding = decodeType
            html_source = response.content.decode(decodeType)
        except:
            print 'decode error'
            response.encoding = 'gbk'
            html_source = response.content
        return html_source

    def get_html_content(self):
        soup = bs(self.html_source, "html.parser")
        content = soup.find("div", attrs={"id":"content"})
        content = str(content).replace('<div id="content"><script>readx();</script>', "")\
            .replace("</div>", "").replace("<br/><br/>", "\r\n")
        return content


    def get_chapter_content(self):
        if self.doc is None:
            return
        '''
        获取章节内容
        根据不同的来源选择不同的处理
        :return:
        '''
        if 'www.qu.la' in self.chapter_url:
            return self.get_qu_chapter_content()
        return

    def get_qu_chapter_content(self):
        return str(self.doc.find("div", attrs={'id': 'content'}).text).replace("readx(); ", "")

    def get_previous_chapter(self):
        '''
        获取上一章节的完整url
        根据不同的来源选择不同的处理
        :return:
        '''
        if 'www.qu.la' in self.chapter_url:
            return self.get_qu_previous_chapter()
        return

    def get_qu_previous_chapter(self):
        if self.doc is None:
            return
        result = self.doc.find('a', text="上一章")["href"]
        if not result in self.chapter_url:
            result = os.path.dirname(self.chapter_url) + '/' + result
        else:
            result = 'http://www.qu.la' + result
        return result

    def get_next_chapter(self):
        '''
        获取下一章节的完整url
        根据不同的来源选择不同的处理
        :return:
        '''
        if 'www.qu.la' in self.chapter_url:
            return self.get_qu_next_chapter()
        return

    def get_qu_next_chapter(self):
        if self.doc is None:
            return
        result = self.doc.find('a', text="下一章")["href"]
        if not result in self.chapter_url:
            result = os.path.dirname(self.chapter_url) + '/' + result
        else:
            result = 'http://www.qu.la' + result
        return result

if __name__ == '__main__':
    chapter= Chapter("http://www.qu.la/book/27933/10312055.html")
    print chapter.get_html_content()