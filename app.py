from flask import Flask,session,g
import config
import os
from exts import db,mail
from models import UserModel,QuestionModel,EmailCaptchModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

app = Flask(__name__,
            instance_path=os.path.join(os.getcwd(), 'instance'),
            static_folder='static',
            template_folder='templates')


# 绑定配置
app.config.from_object(config)


db.init_app(app)
mail.init_app(app)

migrate = Migrate(app,db)

# blueprint: 用来做模块化的
# 电影、读书、音乐、xxx
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

# before_request/before_first_request/after_request
# hook
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)

@app.context_processor
def my_context_processor():
    return {"user": g.user}


# 在注册blueprints之后添加以下代码：
def check_and_init_db():
    from sqlalchemy import inspect
    from sqlalchemy.exc import OperationalError
    # 获取所有需要检查的模型
    models_to_check = [UserModel, QuestionModel, EmailCaptchModel]

    try:
        with app.app_context():
            # 手动创建数据库表
            print("🔄 尝试创建数据库表...")
            db.create_all()
            print("✅ 数据库表创建完成")

            # 添加初始数据
            if not UserModel.query.first():
                print("🆕 创建默认用户...")
                default_user = UserModel(username="管理员", email="admin@example.com",
                                         password=generate_password_hash("admin123"))
                db.session.add(default_user)
                db.session.commit()
                print("🆗 默认用户创建完成")

    except OperationalError as e:
        print(f"⚠️ 数据库连接错误: {e}")
    except Exception as e:
        print(f"🔴 数据库初始化失败: {e}")


# 立即执行数据库初始化
check_and_init_db()
application = app


if __name__ == '__main__':
    # app.run()
    application.run()
#     app.run(debug=False)

# 移除 if __name__ == '__main__': 块
# 在文件最后添加：
# application = app  # 重命名为 application

