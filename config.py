# -*- coding: utf-8 -*-
# @Time    : 2025/6/25 16:49
# @Author  : 荒
# @FileName: config.py
# @Software: PyCharm

# SECRET_KEY = "binglianshang"
#
# # 数据库的配置信息
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'QAPlatform'
# USERNAME = 'root'
# PASSWORD = 'root'
# DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
# # DB_URI = "mysql+pymysql://root:FQAaMlJgHzmLkVhrjFwOAZNXmIrQXGbR@mainline.proxy.rlwy.net:16309/railway"
# SQLALCHEMY_DATABASE_URI = DB_URI
# # SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
#
# # 邮箱配置
# MAIL_SERVER = "smtp.qq.com"
# MAIL_USE_SSL = True
# MAIL_PORT = 465
# MAIL_USERNAME = "2213713266@qq.com"
# MAIL_PASSWORD = "ltcqibyristidjbj"
# MAIL_DEFAULT_SENDER = "2213713266@qq.com"

import os


class Config:
    # 解决Vercel上静态文件路径问题
    if os.getenv('VERCEL'):
        STATIC_FOLDER = os.path.join(os.getcwd(), 'static')
    else:
        STATIC_FOLDER = 'static'

    STATIC_URL_PATH = '/static'

    SECRET_KEY = os.environ.get('SECRET_KEY', 'binglianshang')

    # 使用环境变量配置数据库
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:root@127.0.0.1:3306/QAPlatform?charset=utf8mb4')
    # 处理数据库URL
    DATABASE_URL = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')
    # Vercel Postgres的特殊处理
    if 'vercel-storage.com' in DATABASE_URL:
        # 替换适配SQLAlchemy
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace(
            'postgres://',
            'postgresql+psycopg2://',
            1
        ) + "?sslmode=require"
    else:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL


    # 邮箱配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER', "smtp.qq.com")
    MAIL_PORT = os.environ.get('MAIL_PORT', 465)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', "2213713266@qq.com")
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', "ltcqibyristidjbj")
    MAIL_DEFAULT_SENDER =  os.environ.get("MAIL_DEFAULT_SENDER","2213713266@qq.com")
