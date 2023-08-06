# -*- coding: utf-8 -*-
import requests
import json
import time
import hmac
import urllib
import base64
import hashlib
import sys
import oss2
import random
import string
import os
import psycopg2.extras
import psycopg2 as pg
import ast
import imgkit
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
# psycopg2-binary下载<2.9版本的；>=2.9版本的，copy_from做了调整
# pip install psycopg2-binary==2.8.6


class DingBot:
    def __init__(self):
        # ----------- 当前执行路径 -----------
        if getattr(sys, 'frozen', False):
            # frozen
            self.dir_ = os.path.dirname(sys.executable)
        else:
            # unfrozen
            self.dir_ = os.path.dirname(os.path.realpath(__file__))

        # ----------- 机器人相关参数 -----------
        self.url = None
        self.sec = None
        self.bot_msg = ''
        # 消息标题(消息中不体现, 未进入聊天界面时展示的内容)
        self.msg_title = '-'
        # 图片标题
        self.img_title = ''
        # 图片为空时,是否需要发送消息
        self.img_null_is_send = True

        # ----------- oss参数 -----------
        self.access_key_id = None
        self.access_key_secret = None
        self.endpoint = 'http://oss-ap-southeast-1.aliyuncs.com'
        self.bucket_name = 'surfin-bigdata'

    def set_kwargs(self, **kwargs):
        for k, v in kwargs.items():
            # -------------- 机器人配置 --------------
            #  'url'和'access_token'2选1即可
            #  都设置则只生效后设置的值
            if k in ('W     ebhook', 'url', 'bot_url', 'access_token'):
                self.set_bot_url(v)
            if k == 'access_token':
                self.set_bot_access_token(v)
            if k in ('sec', 'secret', 'bot_sec'):
                self.set_bot_sec(v)

            # -------------- oss配置 ---------------
            if k in ('access_key_id', 'key_id'):
                self.set_oss_access_key_id(v)
            if k in ('access_key_secret', 'key_secret'):
                self.set_oss_access_key_secret(v)
            if k == 'endpoint':
                self.set_oss_endpoint(v)
            if k == 'bucket_name':
                self.set_oss_bucket_name(v)

            # -------------- 其他 ------------------
            if k == 'img_title':
                self.set_img_title(v)
            if k == 'msg_title':
                self.set_msg_title(v)
            if k == 'img_null_is_send':
                self.set_img_null_is_send(v)

    def set_oss_access_key_id(self, v: str):
        self.access_key_id = v

    def set_oss_access_key_secret(self, v: str):
        self.access_key_secret = v

    def set_oss_endpoint(self, v: str):
        self.endpoint = v

    def set_oss_bucket_name(self, v: str):
        self.bucket_name = v

    def set_msg_title(self, v: str):
        self.msg_title = v

    def set_img_title(self, v: str):
        self.msg_title = v

    def set_bot_access_token(self, v: str):
        self.url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % v

    def set_bot_url(self, v: str):
        self.url = v
        self.set_bot_sec(self.sec) if self.sec else None

    def set_img_null_is_send(self, v: bool):
        self.img_null_is_send = v

    def set_bot_sec(self, v: str):
        self.sec = v
        if self.url:
            # 有密钥，需要对url处理后重新赋值
            timestamp = str(int(round(time.time() * 1000)))
            secret_enc = self.sec.encode('utf-8')
            string_to_sign = '{}\n{}'.format(timestamp, self.sec)
            string_to_sign_enc = string_to_sign.encode('utf-8')
            hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
            if str(sys.version).startswith('2.'):
                sign = urllib.pathname2url(base64.b64encode(hmac_code))
            else:
                sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
            self.url = "%s&timestamp=%s&sign=%s" % (self.url, str(timestamp), sign)

    def set_bot_msg(self, v: str):
        self.bot_msg = v

    def append_bot_msg(self, v: str):
        self.bot_msg += v

    def __check(self, func_type='text'):
        if not self.url:
            raise ValueError('not found url')
        if func_type == 'send_img':
            if not self.access_key_id:
                raise ValueError('not found access_key_id')
            if not self.access_key_secret:
                raise ValueError('not found access_key_secret')

    def send_text(self, msg=''):
        self.__check()
        self.bot_msg += msg
        headers = {"Content-Type": "application/json;charset=utf-8"}
        data = {
            "msgtype": 'text',
            "text": {
                "content": self.bot_msg  # 需要发的消息
            }
        }
        result = requests.post(self.url, data=json.dumps(data), headers=headers)
        return result.text

    # noinspection PyBroadException
    def __pg_fetchall(self, pg_config, pg_sql, connect_timeout=10, re_cnt=3):
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
            time.sleep(5)
            return self.__pg_fetchall(pg_config, pg_sql,  connect_timeout=connect_timeout, re_cnt=re_cnt-1)
        cur.execute(pg_sql)
        result_data = cur.fetchall()
        conn.commit()
        conn.close()
        return result_data

    def __data2url(self, result_data, html_path, img_path, oss_img_name):
        # ----- 数据转html文件 -----
        self.__data2html(result_data, html_path, img_title=self.img_title)

        # ----- html转本地图片 -----
        try:
            imgkit.from_file(html_path, img_path)
        finally:
            os.remove(html_path) if os.path.exists(html_path) else None

        # ----- 本地图片上传到云 -----
        try:
            img_url = self.__oss_img_up(img_path=img_path, oss_img_name=oss_img_name)
        finally:
            os.remove(img_path) if os.path.exists(img_path) else None
        return img_url

    def send_img_simple(self, pg_config, pg_sql):
        self.__check(func_type='send_img')

        # ----- 获取数据 -----
        result_data = self.__pg_fetchall(pg_config, pg_sql)

        # ----- 数据转图片url ------
        html_path = "%s/data2html%s.html" % (self.dir_,
                                             ''.join([random.choice(string.ascii_lowercase) for i in range(0, 32)]))
        img_path = '%s/html2jpg%s.jpg' % (self.dir_,
                                          ''.join([random.choice(string.ascii_lowercase) for i in range(0, 32)]))
        oss_img_path = 'temp_sf_etl/url%s' % ''.join([random.choice(string.ascii_lowercase) for i in range(0, 32)])
        if result_data:
            img_url = self.__data2url(result_data, html_path, img_path, oss_img_path)
        elif self.img_null_is_send:
            img_url = ''
        else:
            return 'data is null'

        # ----- 发送钉钉 -----
        try:
            headers = {"Content-Type": "application/json;charset=utf-8"}
            data = {
                "msgtype": 'markdown',
                "markdown": {
                    "picUrl": img_url,
                    "title": self.msg_title,
                    "text": "%s \n![screenshot](%s) \n" % (self.bot_msg, img_url)
                }
            }
            result = requests.post(self.url, data=json.dumps(data), headers=headers)
        finally:
            self.__oss_img_up(is_del=True, oss_img_name=oss_img_path)
        return result.text

    def __oss_img_up(self, img_path=None,
                     oss_img_name=None,
                     is_del=False):
        if (img_path is None or oss_img_name is None) and is_del is False:
            return False
        # 阿里云oss账号
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        if is_del:
            # 删除已上传的图片
            bucket.delete_object(oss_img_name)
            return True
        else:
            bucket.put_object_from_file(oss_img_name, img_path)
            fig_url = bucket.sign_url('GET', oss_img_name, 20000)
            return str(fig_url)

    @staticmethod
    def __data2html(data, img_path, img_title=""):
        table = Table()
        headers = data[0].keys()
        rows = [i.values() for i in data]
        table.add(headers, rows)
        table.set_global_opts(
            # title_opts=ComponentTitleOpts(title="Table-基本示例", subtitle="我是副标题支持换行哦")
            title_opts=ComponentTitleOpts(title=img_title)
        )
        table.render(path=img_path)
        return img_path
