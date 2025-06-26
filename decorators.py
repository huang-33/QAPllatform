# -*- coding: utf-8 -*-
# @Time    : 2025/6/26 17:04
# @Author  : 荒
# @FileName: decorators.py
# @Software: PyCharm

from functools import wraps
from flask import g,redirect,url_for

def login_required(func):
    # 保留func的信息
    @wraps(func)
    def inner(*args,**kwargs):
        if g.user:
            return func(*args,**kwargs)
        else:
            return redirect(url_for("auth.login"))
    return inner