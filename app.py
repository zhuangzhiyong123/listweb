from flask import request, url_for, redirect, flash, Flask, render_template
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的name值
        if (not title) or (len(title) > 60):
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST': # 处理编辑表单的提交请求
        title = request.form['title']
        if not title or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))
        # 重定向回对应的编辑页面
        movie.title = title # 更新标题
        db.session.commit() # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index')) # 重定向回主页
    return render_template('edit.html', movie=movie) # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST']) #限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id) # 获取电影记录
    db.session.delete(movie) # 删除对应的记录
    db.session.commit() # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index')) # 重定向回主页


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


app.config['SECRET_KEY'] = 'dev'

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
