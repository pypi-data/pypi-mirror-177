# -*- coding: utf-8 -*-

import time
import psycopg2
import pymysql


RECONNECT_TIME_GAP = 10
RECONNECT_TIMES = 5


class DbConnection(object):

    def __init__(self, dbconfig):
        self.host = dbconfig['host']
        self.port = dbconfig['port']
        self.user = dbconfig['user']
        self.password = dbconfig['password']
        self.dbname = dbconfig['dbname']
        self.db_type = dbconfig['db_type']

    def get_connection(self):
        if self.db_type == 'pg':
            return psycopg2.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    password=self.password,
                                    database=self.dbname)
        if self.db_type == 'mysql':
            return pymysql.connect(host=self.host,
                                   port=self.port,
                                   user=self.user,
                                   password=self.password,
                                   database=self.dbname)

    def reconnect(self, time_gap, reconnect_times):
        number = 0
        while number < reconnect_times:
            try:
                print('Try to reconnect, this is the ', number, 'times')
                conn = self.get_connection()
                print('Reconnect successful')
                return conn
            except:
                if number == reconnect_times - 1:
                    raise
                else:
                    number = number + 1
                    time.sleep(time_gap)
                    continue

    def close(self, connection):
        connection.close()


def connect_check(connection, conf, time_gap=RECONNECT_TIME_GAP, reconnect_times=RECONNECT_TIMES):
    try:
        cur = connection.cursor()
        check_connection_sql = 'select 1;'
        cur.execute(check_connection_sql)
        return connection
    except:
        conn_sid = DbConnection(conf)
        try:
            connection = conn_sid.reconnect(time_gap, reconnect_times)
            return connection
        except Exception as e:
            print(e)
            print('此处需要配置报警')  # 微信
            # msg = wx_msg.str_replace(wx_msg.RECONNECT_FAILED_MSG,
            #                          {'$reconnect_times': str(reconnect_times), '$time_gap': str(time_gap),
            #                           '$host': str(conf['host']), '$port': str(conf['port']),
            #                           '$user': str(conf['user']), '$exception': str(e)})
            # wx_msg.send_robot(msg)
            return None