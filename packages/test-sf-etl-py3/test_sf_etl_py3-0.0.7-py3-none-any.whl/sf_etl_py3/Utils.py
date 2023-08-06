# -*- coding: utf-8 -*-
import time
import datetime
import oss2
import ast
import psycopg2.extras
import psycopg2 as pg


def get_time(day=0, utc=8.0, time_type='timestamp'):
    """
    :param
        day: 0 当天, 1 第二天, -1 昨天
        utc: 时区, 默认北京时间
        time_type: 返回的数据样式,可选: unix timestamp date
    :return
        字符串
    """
    now_time = int(time.time()) + (day * 86400)  # 当前对应的时间戳
    utc_time = datetime.datetime.utcfromtimestamp(now_time + utc * 3600)
    if time_type == 'unix':
        return str(now_time)
    if time_type == 'date':
        return str(utc_time.strftime("%Y-%m-%d"))
    return str(utc_time.strftime("%Y-%m-%d %H:%M:%S"))


class SfOss:
    def __init__(self):
        self.access_key_id = None
        self.access_key_secret = None
        self.endpoint = 'http://oss-ap-southeast-1.aliyuncs.com'
        self.bucket_name = 'surfin-bigdata'
        self.local_file_path = None
        self.oss_file_path = None
        self.local_data = None

    def set_kwargs(self, **kwargs):
        for k, v in kwargs.items():
            # -------------- oss配置 ---------------
            if k in ('access_key_id', 'key_id'):
                self.set_oss_access_key_id(v)
            if k in ('access_key_secret', 'key_secret'):
                self.set_oss_access_key_secret(v)
            if k == 'endpoint':
                self.set_oss_endpoint(v)
            if k == 'bucket_name':
                self.set_oss_bucket_name(v)

    def set_oss_access_key_id(self, v: str):
        self.access_key_id = v

    def set_oss_access_key_secret(self, v: str):
        self.access_key_secret = v

    def set_oss_endpoint(self, v: str):
        self.endpoint = v

    def set_oss_bucket_name(self, v: str):
        self.bucket_name = v

    def oss_del(self, oss_file_path=None):
        if oss_file_path is None:
            oss_file_path = self.oss_file_path
        # 阿里云oss账号
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        bucket.delete_object(oss_file_path)

    def oss_up_file(self, oss_file_path=None, local_file_path=None):
        if local_file_path is None:
            local_file_path = self.local_file_path
        if oss_file_path is None:
            oss_file_path = self.oss_file_path
        # 阿里云oss账号
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        bucket.put_object_from_file(oss_file_path, local_file_path)
        fig_url = bucket.sign_url('GET', oss_file_path, 20000)
        return str(fig_url)

    def oss_up_data(self, oss_file_path=None, local_data=None):
        if local_data is None:
            local_data = self.local_data
        if oss_file_path is None:
            oss_file_path = self.oss_file_path
        # 阿里云oss账号
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        put_obj = bucket.put_object(oss_file_path, local_data)
        tag = put_obj.headers['ETag']
        fig_url = bucket.sign_url('GET', tag, 20000)
        return str(fig_url)


# noinspection PyBroadException
def pg_fetchall(pg_config, pg_sql, connect_timeout=10, re_cnt=1):
    if isinstance(pg_config, str):
        pg_config = ast.literal_eval(pg_config)
    if 'connect_timeout' in pg_config.keys():
        pass
    else:
        pg_config['connect_timeout'] = connect_timeout
    try:
        conn = pg.connect(**pg_config)
        cur = conn.cursor(cursor_factory=pg.extras.RealDictCursor)
    except Exception:
        if re_cnt <= 0:
            raise ValueError('pg connect timeout')
        time.sleep(3)
        return pg_fetchall(pg_config, pg_sql, connect_timeout=connect_timeout, re_cnt=re_cnt - 1)
    cur.execute(pg_sql)
    result_data = cur.fetchall()
    conn.commit()
    conn.close()
    return result_data


# noinspection PyBroadException
def pg_execute(pg_config, pg_sql, connect_timeout=10, re_cnt=1):
    if isinstance(pg_config, str):
        pg_config = ast.literal_eval(pg_config)
    if 'connect_timeout' in pg_config.keys():
        pass
    else:
        pg_config['connect_timeout'] = connect_timeout
    try:
        conn = pg.connect(**pg_config)
        cur = conn.cursor(cursor_factory=pg.extras.RealDictCursor)
    except Exception:
        if re_cnt <= 0:
            raise ValueError('pg connect timeout')
        time.sleep(3)
        return pg_fetchall(pg_config, pg_sql, connect_timeout=connect_timeout, re_cnt=re_cnt - 1)
    cur.execute(pg_sql)
    conn.commit()
    conn.close()
    return None


def delete_zero_after_point(v):
    s = str(v)
    if '.' in s:
        if len(s.split('.')) == 2:
            l_s = s.split('.')[0]
            r_s = s.split('.')[1].rstrip('0')
            return '%s.%s' % (l_s, r_s)
    return s
