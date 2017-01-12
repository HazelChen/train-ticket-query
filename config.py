#-*- coding:utf-8 -*-
import logging

# 数据库配置
db_host = 'localhost'
db_username = 'root'
db_password = ''
db_table_name = 'trainquery'

# log配置
log_level = logging.INFO
log_format = '%(asctime)s  %(levelname)s %(message)s'
log_datefmt = '%Y %b %d %H:%M:%S'
log_filename = '12306.log'
log_filemode = 'a'

# 脚本运行间隔设置，单位为秒
timegap_free = 3600 # 闲时间隔
timegap_busy = 60 # 忙时间隔

# 邮箱配置
mail_from_addr = ''  # 发送邮箱
mail_from_password = ''  # 发送邮箱密码
mail_smtp_server = 'smtp.qq.com' # 服务器
mail_to_addr = '' # 接收邮箱


