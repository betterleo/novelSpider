# -*- encoding:utf8 -*-

import os
from Config import *
from db import *

conf = config("private_test_db")
db = web.database(dbn=conf.get('dbn'),
                       user=conf.get('user'),
                       pw=conf.get('pw'),
                       host=conf.get('host'),
                       port=conf.get('port'),
                       db=conf.get('db'),
                       charset=conf.get('charset'))
DATABASE_OBJECT = db

# DATABASE_INSTANCE = DB()
#
# CURRENT_PATH = os.getcwd()