import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # 基于安全的考虑，在部署时应该设置为随机字符，且不应该明文写在代码里。
# 注意更新这里的路径，把 app.root_path 添加到 os.path.dirname() 中
# 以便把文件定位到项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

# 设置数据库 URI
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例app
# 初始化 Flask-Login
login_manager = LoginManager(app)  # 实例化扩展类


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchlist.models import User
    user = models.User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


# 如果未登录的用户访问对应的 URL，Flask-Login 会把用户重定向至login_manager.login_view指定的视图端点（函数名）
login_manager.login_view = 'login'
# 通过设置 login_manager.login_message 来自定义错误提示消息。
login_manager.login_message = 'Sorry, please login first.'


# 将user变量统一注入到每一个模板的上下文环境中
@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}


from watchlist import commands, errors, views
