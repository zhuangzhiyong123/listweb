import click

from watchlist import app, db
from watchlist.models import User, Movie


# 自定义命令 initdb，初始化数据库
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


# 注册用户
@app.cli.command()
@click.option('--username', prompt=True, help='The username usedto login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')
