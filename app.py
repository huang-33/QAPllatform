from flask import Flask,session,g
import config
import os
from exts import db,mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

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


# 在注册blueprints之前添加以下代码：
def check_and_init_db():
    from sqlalchemy import inspect
    from models import QuestionModel

    inspector = inspect(db.engine)

    if not inspector.has_table(QuestionModel.__tablename__):
        print("🧰 检测到数据库为空，正在初始化表结构...")
        db.create_all()
        print("✅ 数据库表创建完成")
        # 可选：添加初始数据
        # user = UserModel(...)
        # db.session.add(user)
        # db.session.commit()


with app.app_context():
    # 确保在应用上下文中执行
    check_and_init_db()

application = app


if __name__ == '__main__':
    # app.run()
    application.run()
#     app.run(debug=False)

# 移除 if __name__ == '__main__': 块
# 在文件最后添加：
# application = app  # 重命名为 application

