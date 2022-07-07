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

app = Flask(__name__)
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例app


class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字



class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题


@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)


name = 'zzy'

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
