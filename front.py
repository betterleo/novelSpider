# -*- encoding:utf8 -*-

from db import *
from chapter import *
from CONSTANTS import *


class front:

    def get_novel_list_for_index(self):
        sql = '''select * from novel t ORDER BY RAND() limit 20; '''
        res = []
        results = DATABASE_OBJECT.query(sql)
        for result in results:
            temp = {}
            temp['novel_id'] = str(result.novel_id)
            temp['novel_name'] = result.novel_name
            temp['novel_desc'] = result.novel_desc
            temp['author'] = result.author
            temp['img'] = result.img
            temp['novel_url'] = '/book/' + str(result.novel_id)
            res.append(temp)
        return res

    def get_novel_object(self, novel_id):
        sql = '''select * from novel where novel_id = '%s';''' % int(novel_id)
        res = dict()
        res['chapter_list'] = self.get_chapter_list(novel_id)
        results = DATABASE_OBJECT.query(sql)
        for result in results:
            res['novel_id'] = str(result.novel_id)
            res['novel_name'] = result.novel_name
            res['novel_desc'] = result.novel_desc
            res['author'] = result.author
            res['img'] = result.img
        return res

    def get_chapter_list(self, novel_id):
        sql = '''select * from t_chapter where novel_id = '%s';''' % str(novel_id)
        res = []
        results = DATABASE_OBJECT.query(sql)
        for result in results:
            dic = {}
            dic['chapter_name'] = result.chapter_name
            dic['chapter_id'] = str(result.chapter_id)
            res.append(dic)
        return res

    def get_chapter_detail(self, novel_id, chapter_id):
        sql = '''select * from t_chapter where novel_id = '%s' and chapter_id = '%s';''' % (str(novel_id), str(chapter_id))
        results = DATABASE_OBJECT.query(sql)
        chapter_detail = {}
        for result in results:
            chapter_detail['novel_id'] = str(novel_id)
            chapter_detail['chapter_id'] = str(result.chapter_id)
            chapter_detail['chapter_name'] = result.chapter_name
            chapter = Chapter(result.chapter_url)
            if chapter is not None and chapter.html_source is not None:
                chapter_detail['content'] = str(chapter.get_html_content()).split("\r\n")
            else:
                chapter_detail['content'] = result.content
            #chapter_detail['content'] = str(result.content).split(" ")
            # chapter_detail['previous_chapter_id'] = str(result.previous_chapter_id)
            # chapter_detail['next_chapter_id'] = str(result.next_chapter_id)
            chapter_detail['back_to_index'] = '/book/' + str(novel_id)
            chapter_detail['previous_chapter_id'] = '/book/' +  str(novel_id) + '/' + str(result.previous_chapter_id)
            chapter_detail['next_chapter_id'] = '/book/' + str(novel_id) + '/' +  str(result.next_chapter_id)
        return chapter_detail

if __name__ == '__main__':
    # get_data = front()
    # results = get_data.get_novel_object(1)
    # print(results['novel_id'])
    # print(results['novel_name'])
    # print(results['novel_desc'])
    # print(results['author'])
    # chapter_list = (results['chapter_list'])
    # for current_chapter in chapter_list:
    #     print(current_chapter['chapter_name'])
    #     print(current_chapter['chapter_id'])
    # latest_chapter = chapter_list[-1]
    # print('-'*15 + 'latest_chapter' + '-'*15)
    # print(latest_chapter['chapter_name'])
    # print(latest_chapter['chapter_id'])

    front1 = front()
    sql = '''select * from novel;'''
    results = DATABASE_OBJECT.query(sql)
    for result in results:
        novel_id = result.novel_id
        sql1 = '''update novel set img = '%s.jpg' where novel_id = '%s';''' % (novel_id, novel_id)
        front1.db.query(sql1)