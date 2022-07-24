#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
import pandas as pd
import sqlite3
from conf.paths import DB_PATH


class Sqlite(object):
    def __init__(self):
        self.__conn = sqlite3.connect(DB_PATH)
        self.__cursor = self.__conn.cursor()

    @staticmethod
    def _insert_stmt(table, dicts):
        if len(dicts) <= 0:
            return None, None
        #
        fields = list(dicts[0].keys())
        stmt = "INSERT INTO {table} ({fields}) VALUES ({values})".format(
            table=table,
            fields=",".join(fields),
            values=",".join(["?" for i in range(len(fields))])
        )
        values = list()
        for d in dicts:
            values.append(tuple(d.values()))
        return stmt, values

    @staticmethod
    def _update_stmt(table, dicts, primary_key="id"):
        stmt = []
        template = "UPDATE {table} SET %s WHERE {primary_key}=%s".format(table=table, primary_key=primary_key)
        for d in dicts:
            _template = template + ''
            stmt.append(
                _template % (",".join(["%s='%s'" % (k, d[k]) for k in d.keys() if k != primary_key]), d[primary_key]))
        return stmt

    def insert_sql(self, sql):
        self.__cursor.execute(sql)
        self.__conn.commit()

    def insert_many(self, table, dicts):
        stmt, values = self._insert_stmt(table, dicts)
        if stmt is None or values is None:
            return
        #
        win, size = 100, len(values)
        for i in range(math.ceil(size/win)):
            self.__cursor.executemany(stmt, values[i*win:min((i+1)*win, size)])
        self.__conn.commit()

    def select(self, sql):
        return self.__cursor.execute(sql).fetchall()

    def count(self, table, where=''):
        return self.__cursor.execute('SELECT count(*) FROM `%s` %s' %
                                     (table, '' if not where else 'WHERE '+where)).fetchone()[0]

    def truncate(self, table):
        self.__cursor.execute('DELETE FROM %s' % table)
        self.__cursor.execute('DELETE FROM SQLITE_SEQUENCE WHERE name="%s"' % table)
        self.__conn.commit()

    def dump(self, table, filepath):
        df = pd.read_sql_query("SELECT * FROM `%s`" % table, self.__conn)
        df.to_csv(filepath, index=False)

    def close(self):
        self.__conn.close()


if __name__ == '__main__':
    sqlite = Sqlite()
    sqlite.truncate('crawlstat')
    sqlite.truncate('extractor')
    # print(sqlite.select('SELECT DISTINCT resp_code FROM %s ORDER BY resp_code' % 'crawlstat'))
    sqlite.close()

