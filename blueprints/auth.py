# -*- coding: utf-8 -*-
# @Time    : 2025/6/25 16:52
# @Author  : 荒
# @FileName: auth.py
# @Software: PyCharm

from flask import Blueprint,render_template,jsonify,redirect,url_for,session
from flask_mail import Message
from exts import mail,db
from flask import request
import string
import random
from models import EmailCaptchModel
from .forms import RegisterForm,LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash,check_password_hash

# /auth
bp = Blueprint("auth",__name__,url_prefix="/auth")


@bp.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("该邮箱未注册")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password,password):
                # cookie:
                # cookie中不适合存储太多的数据，只适合存储少量的数据
                # cookie一般可以用来存放登录授权的东西
                # flask中的session，是经过加密后存储再cookie中的
                session["user_id"] = user.id
                return redirect("/")
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


# GET: 从服务器上获取数据
# POST：将客户端的数据提交给服务器
@bp.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf：wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email,username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# bp.route: 如果没有指定methods参数，默认就是GET请求(POST)
@bp.route("/captcha/email",methods=["GET"])
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx@qq.com
    email = request.args.get("email")
    # 4/6: 随机数字、字母、数字和字母的组合
    source = string.digits * 4
    captcha = random.sample(source,4)
    captcha = "".join(captcha)
    message = Message(subject="问答平台注册验证码",recipients=[email],body=f"您的验证码是：{captcha}")
    mail.send(message)
    # memcached/redis
    # 用数据库的方式存储
    email_captcha = EmailCaptchModel(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTful API
    # {code: 200/400/500,message: "",data:{}}
    return jsonify({"code": 200,"message": "","data":None})

# 3564769524@qq.com
@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试",recipients=["2213713266@qq.com"],body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功！"