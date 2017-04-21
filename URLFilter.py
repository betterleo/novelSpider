# -*- encoding:utf8 -*-


class URLFilter:
    def __init__(self, url):
        self.source_url = url
        self.prefix = self.get_host_prefix()
        self.host_url = self.get_host_url()
        pass

    def get_host_prefix(self):
        '''
        获取网址的前缀
        :return:
        '''
        if str(self.source_url).startswith('https://'):
            return 'https://'
        else:
            return 'http://'

    def get_host_name(self):
        '''
        获得网站英文网址，即除去前缀和/
        :return:
        '''
        if str(self.source_url).__contains__(self.get_host_prefix()):
            return str(self.source_url).replace(self.get_host_prefix(), '').split('/')[0]
        else:
            return str(self.source_url).split('/')[0]

    def get_host_url(self):
        '''
        获取网站的url
        :return:
        '''
        host_url = self.prefix + self.get_host_name()
        return host_url

    def get_url_end(self):
        '''
        获取网址的最后一个内容
        :return:
        '''
        return str(self.source_url).split('/')[-1]

    def get_novel_temp_url(self):
        '''
        获取小说的相对路径
        :return:
        '''
        temp_url = self.source_url
        if str(temp_url).__contains__('://'):
            temp_url = str(temp_url).replace(self.get_host_prefix(), '')
        temp_url = temp_url.replace(self.get_host_name(), '')
        temp_url = temp_url.replace(self.get_url_end(), '')
        return temp_url

    def get_novel_url(self):
        '''
        获取小说的网址
        :return:
        '''
        return str(self.host_url) + self.get_novel_temp_url()


if __name__ == '__main__':
    url = 'www.qu.la/book/123/1.html'
    u = URLFilter(url)
    print u.get_host_prefix()
    print u.get_host_name()
    print u.get_novel_temp_url()
    print u.get_novel_url()
    print u.get_url_end()
