from flask import Flask, render_template

app = Flask(__name__)


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
          {'title': '一个叫欧维的男人决定去死'},
          {'title': '西西里的美丽传说'},
          {'title': '极速车王'},
          {'title': '阿凡达'},
          ]
