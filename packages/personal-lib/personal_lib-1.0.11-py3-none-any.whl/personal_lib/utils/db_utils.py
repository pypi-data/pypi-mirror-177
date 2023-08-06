import pandas as pd
import pymysql
from pymysql.cursors import DictCursor

conn_pool = {}


def add_connect(host, port, user, passwd, db, name):
    global conn_pool
    db = DBConn(host, port, user, passwd, db, name)
    conn_pool[db.name] = db


def get_conn(name):
    global conn_pool
    current_conn = conn_pool[name]
    return current_conn


class DBConn():
    def __init__(self, host, port, user, passwd, db, name):
        self.name = name
        self.conn = pymysql.connect(user=user, passwd=passwd, host=host, port=port, db=db)
        self.cur = self.conn.cursor(DictCursor)

    def close(self):
        if self.conn is not None:
            self.conn.close()

    def query_data(self, sql, args=None):
        self.cur.execute(sql, args)
        results = self.cur.fetchall()
        df = pd.DataFrame(results)
        return df

    def exec_sql(self, sql, args=None):
        self.cur.execute(sql, args)
        self.conn.commit()

    def exec_many(self, sql, args=None):
        self.cur.executemany(sql, args)
        self.conn.commit()
