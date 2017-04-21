# -*- encoding:utf8 -*-

import requests
from bs4 import BeautifulSoup as bs
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

host = 'www.qu.la'
decodeType = 'gbk'


def get_novel_list(website_url):
    '''
    获取网站的小说列表
    根据不同的来源选择不同的处理
    :return:
    '''
    if 'www.qu.la' in website_url:
        global host, decodeType
        decodeType = 'gbk'
        host = 'http://www.qu.la'
    response = requests.get(website_url)
    if response.status_code != 200:
        return
    data = response.content.decode(decodeType)
    if 'www.qu.la' in website_url:
        return get_qu_novel_list(data)
    return


def get_qu_novel_list(html_source):
    doc = bs(html_source, "html.parser")
    a_list = doc.find_all("a")
    return [item for item in a_list if '/book/' in str(item) and item.text != '' and '.html' not in str(item)]
