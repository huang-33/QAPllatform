# -*- coding: utf-8 -*-
# @Time    : 2025/6/25 16:49
# @Author  : 荒
# @FileName: exts.py
# @Software: PyCharm

# exts.py: 这个文件存在的意义就是为了解决循环引用的问题

# flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()