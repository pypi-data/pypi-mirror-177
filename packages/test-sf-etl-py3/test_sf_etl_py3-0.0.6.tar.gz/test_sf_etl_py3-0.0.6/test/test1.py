# -*- coding: utf-8 -*-
from sf_etl_py3 import Utils, Bot

# # ----- oss参数, 用来存放图片生成url ------
# access_key_id = 'LTAIUPUoum55etcM'
# access_key_secret = 'S5W5mJbxfvonH9pC5OeMtGnfy99jXx'
# bucket_name = 'sg-log-backup'
# # endpoint = 'oss-ap-southeast-1-internal.aliyuncs.com'  # vpn用这个?
# endpoint= 'oss-ap-southeast-1.aliyuncs.com'
#
#
# pg_config = {'host': 'rm-t4ne89z027r9mrz419o.pgsql.singapore.rds.aliyuncs.com', 'port': 3433, 'user': 'etl_user',
#              'password': 'temp4you', 'database': 'dw'}
# pg_sql = 'select * from dim.user limit 2;'
# ding_obj = Bot.DingBot()
# ding_obj.set_kwargs(
#     url='https://oapi.dingtalk.com/robot/send?access_token=7704a2fe812d71c1a6b4b725cc850f12464c3a7e491cc593d87a694716837144',
#     sec='SEC6903bd28016e418a3edb1c32e112b81c37ca1d107ac0d319e7ff5176394bcee1',
#     access_key_id=access_key_id,
#     access_key_secret=access_key_secret,
#     bucket_name=bucket_name,
#     endpoint=endpoint, )
# r = ding_obj.send_img_simple(pg_config, pg_sql)
# print(r)


oss_obj = Utils.SfOss()
oss_obj.set_oss_access_key_id('LTAI5tKYoVtLXzZ8s7QCidwa')
oss_obj.set_oss_access_key_secret('tv0Mo0KTs6yih251tSubteqaS253ue')
# with open('../sf_etl_py3/data2htmltdrgwkmnucibjmvyveowzxocoodjxxsh.html', 'r') as r_obj:
#     local_data = (r_obj.read())
url = oss_obj.oss_up_file('test/testzzz3.html', '../sf_etl_py3/data2htmltdrgwkmnucibjmvyveowzxocoodjxxsh.html')
print(url)

