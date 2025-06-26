# -*- coding: utf-8 -*-
# @Time    : 2025/6/26 23:45
# @Author  : 荒
# @FileName: wsgi.py
# @Software: PyCharm


# 在项目根目录创建 wsgi.py 文件
from app import app

if __name__ == "__main__":
    app.run()
