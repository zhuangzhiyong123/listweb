from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类

# 设置数据库 URI
import os
import sys

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app)  # 初始化扩展，传入程序实例app


class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字u


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题


# 将user变量统一注入到每一个模板的上下文环境中
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}


@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 自定义命令 initdb
import click


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


# 自定义创建虚拟数据命令
@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()
    # 全局的两个变量移动到这个函数内
    user_name = 'zzy'

    movies = [{'title': '这个杀手不太冷'},
              {'title': '十二怒汉'},
              {'title': '堕落天使'},
              {'title': '黑客帝国'},
              {'title': '辛德勒的名单'},
              {'title': '无间道3'},
              {'title': '雷神'},
              {'title': '西西里的美丽传说'},
              {'title': '极速车王'},
              {'title': '阿凡达'},
              ]
    user = User(name=user_name)
    db.session.add(user)

    for m in movies:
        movie = Movie(title=m['title'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')
