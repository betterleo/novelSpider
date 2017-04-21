# -*- encoding:utf8 -*-

conn = dict()


class data:
    private_test_db = {
        'dbn': 'mysql',
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'pw': 'abc123',
        'db': 'novel',
        'charset': 'utf8'
    }


def config(config_name):
    if data.__dict__.get(config_name):
        for k in data.__dict__.get(config_name):
            conn[k] = data.__dict__.get(config_name).get(k)
        return conn
