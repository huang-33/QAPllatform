from flask import Flask,session,g
import config
import os
from exts import db,mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
# 使用绝对路径解决模板路径问题
app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


# 绑定配置
# app.config.from_object(config)

# 优先使用Vercel环境变量
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', config.SQLALCHEMY_DATABASE_URI)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', config.SECRET_KEY)
app.config['MAIL_*'] = {  # 邮件配置也使用环境变量
    'MAIL_SERVER': os.environ.get('MAIL_SERVER', config.MAIL_SERVER),
    'MAIL_USE_SSL': os.environ.get('MAIL_USE_SSL', config.MAIL_USE_SSL),
    'MAIL_PORT': os.environ.get('MAIL_PORT', config.MAIL_PORT),
    'MAIL_USERNAME': os.environ.get('MAIL_USERNAME', config.MAIL_USERNAME),
    'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD', config.MAIL_PASSWORD),
    'MAIL_DEFAULT_SENDER': os.environ.get('MAIL_DEFAULT_SENDER', config.MAIL_DEFAULT_SENDER),
}


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

# Vercel特定入口函数
def vercel_handler(request):
    with app.app_context():
        response = app.full_dispatch_request(request)
    return response

@app.route('/debug')
def debug():
    return {
        'current_dir': os.getcwd(),
        'files': os.listdir(),
        'templates_exists': os.path.exists('templates'),
        'templates_files': os.listdir('templates') if os.path.exists('templates') else []
    }

if __name__ == '__main__':
    app.run()
