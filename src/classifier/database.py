import json
import leveldb
import functools
import gopage.util
from flask import g
from os.path import join, dirname


class Database:
    name2db = {}
    dbdir = join(dirname(dirname(dirname(__file__))), 'db')
    gopage.util.mkdir(dbdir)

    def __init__(self, name):
        self.db = None
        self.name = 'db_{}'.format(name)
        self.path = join(self.dbdir, self.name)

    def ensure_db(self):
        if self.name not in self.name2db:
            try:
                self.db = leveldb.LevelDB(self.path)
                self.name2db[self.name] = self.db
            except Exception:
                pass

    def get(self, key):
        self.ensure_db()
        try:
            key = key.encode('utf-8')
            ret = self.db.Get(key)
            return json.loads(ret.decode('utf-8'))
        except Exception:
            return None

    def put(self, key, value):
        self.ensure_db()
        key = key.encode('utf-8')
        if isinstance(value, str):
            self.db.Put(key, value)
        else:
            self.db.Put(key, json.dumps(value).encode('utf-8'))

# def cache():
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kw):

#             ret = func(*args, **kw)
#             return ret
#         return wrapper
#     return decorator
