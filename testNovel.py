# -*- encoding:utf8 -*-

from novel import *
from CONSTANTS import *
from chapter import *
import datetime,time


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def insert_all_novel():
    results = DATABASE_OBJECT.query('''select * from website;''')
    for result in results:
        website_url = result.website_url
        # 根据小说网站获取小说url 和名称列表
        novel_list = get_novel_list(website_url)
        for novel in novel_list:
            # 拼接小说url
            novel_url = 'http://'+host + novel['href']
            DATABASE_INSTANCE = DB()
            is_exist = DATABASE_INSTANCE.check_novel_exist(novel_url)
            if is_exist:
                continue
            novel_name = novel.text
            novel = Novel(novel_url)
            novel_id = novel.novel_id
            if novel is None:
                continue
            # 输出小说作者
            author = novel.author
            # 输出小说介绍
            intro = novel.intro
            # 获取最新章节对象
            latest_chapter = novel.get_chapter_list()[0]
            # 获取最新章节url
            latest_chapter_url = novel_url + latest_chapter['href']
            # 获取最新章节名称
            latest_chapter_name = latest_chapter.text
            img = save_img(novel_id, novel.get_novel_img())
            DATABASE_INSTANCE.insert_novel_to_db(novel_name, novel_url, author, intro,
                                           latest_chapter_name, latest_chapter_url, img)


def check_novel_and_update_latest_chapter():
    results = DATABASE_OBJECT.query('''select * from novel;''')
    for result in results:
        novel_url = result.novel_url
        novel_id = result.novel_id
        last_latest_chapter_url = result.latest_chapter_url
        last_latest_chapter_name = result.latest_chapter_name
        novel = Novel(novel_url)
        if novel is None:
            continue
	try:
		novel_chapter_list_ = novel.get_chapter_list()
		#print(novel_chapter_list_)
        	latest_chapter = novel_chapter_list_[0]
	except:
		novel = Novel(novel_url)
		novel_chapter_list_ = novel.get_chapter_list()
                #print(novel_chapter_list_)
        # 获取最新章节url
        latest_chapter_url = novel_url + latest_chapter['href']
        # 获取最新章节名称
        latest_chapter_name = latest_chapter.text
        dt = get_current_time()
        print(latest_chapter_url)
        print(last_latest_chapter_url)
        print(latest_chapter_name)
        print(last_latest_chapter_name)
        if str(latest_chapter_url) != str(last_latest_chapter_url) or str(latest_chapter_name) != str(
                last_latest_chapter_name):
            DATABASE_INSTANCE = DB()
            DATABASE_INSTANCE.update_latest_chapter_in_novel(novel_id, latest_chapter_url, latest_chapter_name)


def check_chapter_and_update_chapter():
    results = DATABASE_OBJECT.query('''select * from novel;''')
    for result in results:
        novel_url = result.novel_url
        novel_id = result.novel_id
        # if novel_id <225:
        #     continue
        novel = Novel(novel_url)
        while novel is None or not novel.__dict__.has_key('doc'):
            novel = Novel(novel_url)
        # 获取全部章节
        chapter_list = novel.get_chapter_list()[1:]
        chapter_results = DATABASE_OBJECT.query('''select chapter_url from chapter where novel_id='%s';''' % novel_id)
        chapter_lst = list()
        for chapter_result in chapter_results:
            chapter_lst.append(chapter_result.chapter_url)
        # # 遍历列表
        for item in chapter_list:
            if item is None:
                continue
            # 获取章节url
            chapter_url = novel_url + item['href']
            # 获取章节名称
            chapter_name = item.text
            # exist = db_instance.check_chapter_exist(chapter_url)
            if chapter_url in chapter_lst:
                continue
            chapter = Chapter(chapter_url)
            while chapter is None or not chapter.__dict__.has_key('doc'):
                print chapter_url
                print chapter.__dict__.has_key('doc')
                print '再次重试'
                chapter = Chapter(chapter_url)
            content = chapter.get_chapter_content()
            if content is None or chapter.previous_chapter is None or chapter.next_chapter is None:
                continue
            #DATABASE_INSTANCE.insert_chapter_to_db(novel_id, chapter_name, chapter_url, content, chapter.get_previous_chapter(), chapter.get_next_chapter())
            DATABASE_INSTANCE = DB()
            DATABASE_INSTANCE.insert_chapter_to_db(novel_id, chapter_name, chapter_url, None,
                                                   chapter.get_previous_chapter(),
                                                   chapter.get_next_chapter())


def update_chapter_next_id():
    results = DATABASE_OBJECT.query('''select * from novel;''')
    for result in results:
        novel_url = result.novel_url
        novel_id = result.novel_id
        chapter_results = DATABASE_OBJECT.query('''select * from t_chapter where novel_id='%s';''' % novel_id)
        current_chapter_previous_id = None
        current_chapter_previous_url = None
        for current_chapter in chapter_results:
            previous_chapter_id = current_chapter.previous_chapter_id
            current_chapter_id = current_chapter.chapter_id
            current_chapter_url = current_chapter.chapter_url
            if current_chapter_previous_id is not None and current_chapter_previous_id is not None and previous_chapter_id is None:
                dt = get_current_time()
                DATABASE_OBJECT.update('t_chapter', where='chapter_id=$chapter_id',
                          vars={'chapter_id': current_chapter_previous_id},
                          next_chapter_url=current_chapter_url,
                          next_chapter_id=current_chapter_id, update_time=dt)
                DATABASE_OBJECT.update('t_chapter', where='chapter_id=$chapter_id',
                          vars={'chapter_id': current_chapter_id},
                          previous_chapter_url=current_chapter_previous_url,
                          previous_chapter_id=current_chapter_previous_id, update_time=dt)
            current_chapter_previous_id = current_chapter_id
            current_chapter_previous_url = current_chapter_url


def get_and_insert_chapter():
    results = DATABASE_OBJECT.query('''select * from novel;''')
    for result in results:
        novel_url = result.novel_url
        novel_id = result.novel_id
        # 将数据库中该小说的所有内容获取
        t_chapter_result = DATABASE_OBJECT.query('''select chapter_name, chapter_url from t_chapter where novel_id = '%s';''' % novel_id)
        # 将数据库中已存在的内容放入一个临时列表
        temp_exist_list = []
        for t_chapter in t_chapter_result:
            temp_exist_list.append(t_chapter.chapter_url)

        novel = Novel(novel_url)
        while novel is None or not novel.__dict__.has_key('doc'):
            novel = Novel(novel_url)
        # 获取全部章节
        chapter_list = novel.get_chapter_list()[1:]
        for ch in chapter_list:
            chapter_url = ch['href']
            chapter_name = ch.text
            dt = get_current_time()
            # 如果不在已存在的列表中,则插入数据库
            if novel_url + chapter_url not in temp_exist_list:
                sql = '''INSERT INTO `novel`.`t_chapter` ( `chapter_name`, `chapter_url`, `novel_id`, `create_time`)
                  VALUES ( '%s', '%s','%s', '%s');''' % (chapter_name, novel_url + chapter_url, novel_id, dt)
                DATABASE_OBJECT.query(sql)



if __name__ == '__main__':
    # insert_all_novel()
    # check_novel_and_update_latest_chapter()
    # check_chapter_and_update_chapter()
    # update_chapter_next_id()
    # get_and_insert_chapter()
    # update_chapter_next_id()
    t1 = time.time()
    i = 1
    while(True):
        time.sleep(21)
        print get_current_time()
        t2 = time.time()
        if t2-t1 > 600 or i == 1:
            i = i + 1
            insert_all_novel()
            check_novel_and_update_latest_chapter()
            get_and_insert_chapter()
            update_chapter_next_id()
            t1 = time.time()





