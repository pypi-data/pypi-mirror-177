# # -*- coding: utf-8 -*-
#
# import time
# from io import StringIO
# # from sf_etl_py3.DbConn as db_conn
#
# DATA_SEP = '\u001B'
#
#
# class DbOperations:
#     """DbOperations.db_reoperate(db_config, dboper, **kwargs)
#     db_config 以json类型传入，参数中除常规参数外，还需携带一个额外参数：db_type。
#     dboper 为下面的几个函数，根据需要增删
#     **kwargs 为：需要传入 dboper 的参数
#     """
#
#     # 公共函数 （也可使用装饰函数）
#     def db_reoperate(self, reconn_conf, operate_func, connection=None, **kwargs):
#         query_times = 0
#         while query_times < db_conn.RECONNECT_TIMES:
#             if not connection:
#                 connection = db_conn.connect_check(connection, reconn_conf) # 如果没错，会返回connection，如果有错，无任何返回
#             try:
#                 # print(connection)
#                 return operate_func(connection, **kwargs)
#             except AttributeError as e:
#                 time.sleep(db_conn.RECONNECT_TIME_GAP)
#                 query_times += 1
#                 continue
#             except Exception as e1:
#                 # msg = wx_msg.str_replace(wx_msg.QUERY_FAILED_MSG,
#                 #                          {'$host': str(reconn_conf['host']), '$port': str(reconn_conf['port']),
#                 #                           '$countryname': str(reconn_conf['countryname']),
#                 #                           '$user': str(reconn_conf['user']), '$exception': str(e1)})
#                 # 此处会有异常抛出，需要中断任务，并配置报警
#                 # wx_msg.send_robot(msg)
#                 time.sleep(db_conn.RECONNECT_TIME_GAP)
#                 query_times += 1
#                 # connection = None
#
#         # msg = wx_msg.str_replace(wx_msg.QUERY_FAILED_MSG,
#         #                          {'$host': str(reconn_conf['host']), '$port': str(reconn_conf['port']),
#         #                           '$user': str(reconn_conf['user']), '$exception': '操作数据库失败，请及时处理！'})
#         # 走到这一步，必须要中断任务，并报警
#         # wx_msg.send_robot(msg)
#
#     # 查询数据库
#     def query(self, connection, sql):
#         print('query connection:', connection)
#         cur = connection.cursor()
#         cur.execute(sql)
#         result = cur.fetchall()
#         # connection.commit()
#         cur.close()
#         connection.close()
#         print('connection close')
#         return result
#
#     # dataframe 插入数据库
#     def df_insert(self, connection, dataframe, table_name, columns):
#         print('dataframe insert connection:', connection)
#         output = StringIO()
#         dataframe.to_csv(output, sep=DATA_SEP, index=False, header=False)
#         frame_output = output.getvalue()
#         cur = connection.cursor()
#         cur.execute('SET search_path TO bidba, public')
#         print('SET search_path TO bidba, public')
#         # 如果版本不匹配，会从下面这个开始报错
#         cur.copy_from(StringIO(frame_output), table_name, sep=DATA_SEP, null='', columns=columns)
#         connection.commit()
#         print('commit')
#         cur.close()
#         connection.close()
#         # return connection
#         print('connection close')
#
#     # 正常数据插入数据库
#     def insert(self, connection, sql):
#         print('insert connection:', connection)
#         try:
#             cur = connection.cursor()
#             cur.execute(sql)
#             connection.commit()
#             cur.close()
#         except Exception as e1:
#             result = e1
#         else:
#             result = 'success'
#         print(result)
#         return result
#
#     # 删除操作
#     def delete(self, connection, sql):
#         print('delete connection:', connection)
#         cur = connection.cursor()
#         cur.execute(sql)
#         connection.commit()
#         cur.close()
#         connection.close()
#         print('delete connection:', connection)
#         # return connection
#
#     def modify(self, connection, sql):
#         pass
