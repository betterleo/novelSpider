# -*- encoding:utf8 -*-

import web, datetime

from URLFilter import *
from CONSTANTS import *

def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

global DATABASE_OBJECT
# global database_instance

class DB:

    def create_website_table(self):
        '''
        创建website表
        :return:
        '''
        sql = '''
                CREATE TABLE if not exists `website` (
                  `website_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
                  `website_name` varchar(255) NOT NULL,
                  `website_url` varchar(255) NOT NULL,
                  `website_type` varchar(255) DEFAULT NULL,
                  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
                  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
                  PRIMARY KEY (`website_id`),
                  UNIQUE KEY `n_id` (`website_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
            '''
        DATABASE_OBJECT.query(sql)

    def check_website_exist(self, url):
        '''
        检查网址是否在website中存在
        :param url:
        :return:
        '''
        url_obj = URLFilter(url)
        check_host_url = url_obj.get_host_url()
        results = DATABASE_OBJECT.query('''select * from website where website_url = '%s';''' % check_host_url)
        if len(results) == 0:
            return False
        return True

    def get_website_id(self, url):
        '''
        获取网站的id
        :param url:
        :return:
        '''
        url_obj = URLFilter(url)
        check_host_url = url_obj.get_host_url()
        from CONSTANTS import *
	results = DATABASE_OBJECT.query('''select * from website where website_url = '%s';''' % check_host_url)
        if len(results) == 0:
            return
        for result in results:
            return result.website_id

    def insert_website_to_db(self, url):
        '''
        将网站插入到数据库
        :param url:
        :return:
        '''
        url_obj = URLFilter(url)
        temp_host_url = url_obj.get_host_url()
        host_name = url_obj.get_host_name()
        dt = get_current_time()
        if not self.check_website_exist(url):
            DATABASE_OBJECT.insert('website', website_name=host_name,
                           website_url=temp_host_url, website_type='source', create_time=dt)

    def create_novel_table(self):
        '''
        创建小说表
        :return:
        '''
        sql = '''
            CREATE TABLE if not exists  `novel` (
              `novel_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
              `novel_name` varchar(255) NOT NULL,
              `novel_url` varchar(255) NOT NULL,
              `novel_type` varchar(255) DEFAULT NULL,
              `author` varchar(255) DEFAULT NULL,
              `novel_desc` varchar(2048) DEFAULT NULL,
              `website_id` bigint(20) NOT NULL,
              `latest_chapter_name` varchar(255) DEFAULT NULL,
              `latest_chapter_url` varchar(255) DEFAULT NULL,
              `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
              `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
              PRIMARY KEY (`novel_id`),
              UNIQUE KEY `n_id` (`novel_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

        '''
        DATABASE_OBJECT.query(sql)

    def check_novel_exist(self, novel_url):
        url_obj = URLFilter(novel_url)
        check_novel_url = url_obj.get_novel_url()
        from CONSTANTS import DATABASE_OBJECT
        results = DATABASE_OBJECT.query('''select * from novel where novel_url = '%s';''' % check_novel_url)
        if len(results) == 0:
            return False
        return True

    def insert_novel_to_db(self, novel_name, novel_url,
                           novel_author, novel_desc,
                           latest_chapter_name, latest_chapter_url, img):
        '''
        插入小说到数据库
        :param novel_name: 被抓小说名称
        :param novel_url:   被抓取小说的url
        :param novel_author: 作者
        :param novel_desc:  小说简要介绍
        :param latest_chapter_name: 最新章节名称
        :param latest_chapter_url:  最新章节url
        :return:
        '''
        url_obj = URLFilter(novel_url)
        host_id = self.get_website_id(novel_url)
        check_novel_url = url_obj.get_novel_url()
        dt = get_current_time()
        from CONSTANTS import DATABASE_OBJECT
	# if not self.check_novel_exist(check_novel_url):
        DATABASE_OBJECT.insert('novel', novel_name=novel_name, novel_url=check_novel_url, img=img,
                       author=novel_author, novel_desc=novel_desc, website_id=host_id,
                       latest_chapter_name=latest_chapter_name, latest_chapter_url=latest_chapter_url,
                       novel_type=None, create_time=dt)

    def get_novel_id(self, url):
        url_obj = URLFilter(url)
        check_novel_url = url_obj.get_novel_url()
        from CONSTANTS import *
        results = DATABASE_OBJECT.query('''select * from novel where novel_url = '%s';''' % check_novel_url)
        if len(results) == 0:
            return
        for result in results:
            return result.novel_id

    def create_chapter_table(self):
        sql='''
            CREATE TABLE if not exists `chapter` (
              `chapter_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
              `chapter_name` varchar(255) NOT NULL,
              `chapter_url` varchar(255) NOT NULL,
              `content` TEXT NOT NULL,
              `previous_chapter_url` varchar(255) DEFAULT NULL,
              `next_chapter_url` varchar(2048) DEFAULT NULL,
              `novel_id` bigint(20) NOT NULL,
              `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
              `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
              PRIMARY KEY (`chapter_id`),
              UNIQUE KEY `c_id` (`chapter_id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
        '''
        DATABASE_OBJECT.query(sql)

    def check_chapter_exist(self, chapter_url):
        url_obj = URLFilter(chapter_url)
        check_chapter_url = url_obj.get_novel_url()+url_obj.get_url_end()
        results = DATABASE_OBJECT.query('''select * from chapter where chapter_url = '%s';''' % check_chapter_url)
        if len(results) == 0:
            return False
        return True

    def get_chapter_id(self, url):
        url_obj = URLFilter(url)
        check_chapter_url = url_obj.get_novel_url() + url_obj.get_url_end()
        results = DATABASE_OBJECT.query('''select * from chapter where chapter_url = '%s';''' % check_chapter_url)
        if len(results) == 0:
            return
        for result in results:
            return result.chapter_id

    def insert_chapter_to_db(self, novel_id,chapter_name, chapter_url,
                             content, previous_chapter_url,
                             next_chapter_url):
        url_obj = URLFilter(chapter_url)
        # novel_url = url_obj.get_novel_url()
        # novel_id = self.get_novel_id(novel_url)
        # check_chapter_url = novel_url + url_obj.get_url_end()
        dt = get_current_time()
        print dt
        if not (previous_chapter_url is None or next_chapter_url is None):
            DATABASE_OBJECT.insert('chapter', chapter_name=chapter_name, chapter_url=chapter_url,
                           content=content, previous_chapter_url=previous_chapter_url, next_chapter_url=next_chapter_url,
                           novel_id=novel_id, create_time=dt)

    def update_latest_chapter_in_novel(self, novel_id, latest_chapter_url, latest_chapter_name):
        dt = get_current_time()
        from CONSTANTS import *
        DATABASE_OBJECT.update('novel', where='novel_id=$novel_id', vars={'novel_id': novel_id},
                  latest_chapter_url=latest_chapter_url, latest_chapter_name=latest_chapter_name,
                  update_time=dt)

    def update_next_chapter_in_previous_chapter(self, previous_chapter_url, chapter_url):
        dt = get_current_time()
        DATABASE_OBJECT.update('chapter', where='chapter_url=$previous_chapter_url',
                  vars={'previous_chapter_url': previous_chapter_url},
                  next_chapter_url=chapter_url, update_time=dt)

# if __name__ == '__main__':
#     db = DB()
#     host_url = 'http://www.qu.la'
#     db.insert_website_to_db(host_url)
#     db.create_novel_table()
#     # # db.create_website_table()
#     # s = str(datetime.datetime.now())
#     # print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
