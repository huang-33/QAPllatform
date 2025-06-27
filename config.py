# -*- coding: utf-8 -*-
# @Time    : 2025/6/25 16:49
# @Author  : 荒
# @FileName: config.py
# @Software: PyCharm

SECRET_KEY = "binglianshang"

# 数据库的配置信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'QAPlatform'
USERNAME = 'root'
PASSWORD = 'root'
# DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
DB_URI = "mysql+pymysql://root:FQAaMlJgHzmLkVhrjFwOAZNXmIrQXGbR@mainline.proxy.rlwy.net:16309/railway"
# SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "2213713266@qq.com"
MAIL_PASSWORD = "ltcqibyristidjbj"
MAIL_DEFAULT_SENDER = "2213713266@qq.com"