## **SURFIN 封装一些通用的方法, 要求python3**
> 测试版本
#### pypi地址
https://pypi.org/project/test-sf-etl-py3/
<br><br>

#### 依赖 
发送图片(必须)：需安装wkhtmltopdf,下载地址如下(windows需加入环境变量)  
> https://wkhtmltopdf.org/downloads.html
<br><br>

#### 使用案例
示例：钉钉机器人发送消息
```python
# pip install test_sf_etl_py3
from sf_etl_py3 import Bot

# ------ 发送文本 ------
ding_obj = Bot.DingBot()
ding_obj.set_kwargs(url='*机器人的url',sec='机器人的加签')
ding_obj.send_text('需要发送的消息')

# ------ 发送图片(pg数据库查询到的数据, 以图片形式发送) ------
ding_obj = Bot.DingBot()
ding_obj.set_kwargs(url='*机器人的url',
                    sec='机器人的加签',
                    access_key_id='*阿里云的oss账号',
                    access_key_secret='*阿里云的oss账号',
                    endpoint='阿里云的oss地区, 默认 http://oss-ap-southeast-1.aliyuncs.com',
                    bucket_name='阿里云的ossbucket_name, 默认 surfin-bigdata'
                    )
# 参数1: pg数据库配置
# 需要2: 需要执行的sql   
ding_obj.send_img_simple({'host': 'xxx', 'port': 8756, 'user': 'xxx', 'password': 'xxx', 'database': 'xxx'},
                         "select 1 as test;")
```
<br><br> 
---
#### **版本**
##### 0.0.5
> 测试版本: 增加数据指标波动监控

##### 0.0.0 ~ 0.0.4
> 测试版本: 机器人消息