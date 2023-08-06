# -*- coding: utf-8 -*-
import asyncio
import ast
import psycopg2.extras
import psycopg2 as pg
import time


# noinspection PyBroadException
async def __pg_fetchall(pg_config=None, pg_sql=None, connect_timeout=10, re_cnt=3):
    # pg_config = {'host': 'rm-t4ne89z027r9mrz419o.pgsql.singapore.rds.aliyuncs.com', 'port': 3433, 'user': 'etl_user',
    #              'password': 'temp4you', 'database': 'dw'}
    # pg_sql = 'select * from dim.user limit 2;'
    # if isinstance(pg_config, str):
    #     pg_config = ast.literal_eval(pg_config)
    # if 'connect_timeout' in pg_config.keys():
    #     pass
    # else:
    #     pg_config['connect_timeout'] = connect_timeout
    # try:
    #     conn = pg.connect(**pg_config)
    #     cur = conn.cursor(cursor_factory=pg.extras.RealDictCursor)
    # except Exception:
    #     if re_cnt <= 0:
    #         raise ValueError('pg connect timeout')
    #     time.sleep(5)
    #     return __pg_fetchall(pg_config, pg_sql,  connect_timeout=connect_timeout, re_cnt=re_cnt-1)
    # cur.execute(pg_sql)
    # result_data = cur.fetchall()
    # conn.commit()
    # conn.close()
    # print(result_data)
    # time.sleep(2)
    await asyncio.sleep(1)
    return 1
    # return result_data


async def run_pg():
    print('开始执行')
    a = await __pg_fetchall()
    print('1111')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [run_pg(), run_pg()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


