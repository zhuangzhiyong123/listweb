from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from listweb import db


class User(db.Model, UserMixin):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 验证密码
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题


class Book(db.Model):  # 表名将会是 book
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 书籍标题


class Todo(db.Model):  # 表名将会是 todo
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # todo标题
    ddl = db.Column(db.String(60))  # todo's ddl
