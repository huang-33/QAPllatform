# -*- coding: utf-8 -*-
# @Time    : 2025/6/26 23:44
# @Author  : 荒
# @FileName: vercel_build.py
# @Software: PyCharm

# vercel_build.py
import os
import subprocess


def vercel_build():
    # 安装依赖
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

    # Flask 应用初始化任务（如有需要）
    # ...

    print("Build completed successfully")


if __name__ == '__main__':
    vercel_build()
