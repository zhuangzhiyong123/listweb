from flask import request, url_for, redirect, flash, render_template
from flask_login import current_user, login_required, login_user, logout_user

from listweb import app, db
from listweb.models import User, Movie, Book, Todo


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 判断是否已登录
        if not current_user.is_authenticated:
            redirect(url_for('watchlist'))
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的name值
        if (not title) or (len(title) > 60):
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('watchlist'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('watchlist'))  # 重定向回主页
    movies = Movie.query.all()
    return render_template('watchlist.html', movies=movies)


@app.route('/readlist', methods=['GET', 'POST'])
def readlist():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 判断是否已登录
        if not current_user.is_authenticated:
            redirect(url_for('readlist'))
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的name值
        if (not title) or (len(title) > 60):
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('readlist'))  # 重定向回主页
        # 保存表单数据到数据库
        book = Book(title=title)
        db.session.add(book)
        db.session.commit()
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('readlist'))  # 重定向回主页
    books = Book.query.all()
    return render_template('readlist.html', books=books)


@app.route('/todolist', methods=['GET', 'POST'])
@login_required
def todolist():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 判断是否已登录
        if not current_user.is_authenticated:
            redirect(url_for('todolist'))
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的name值
        ddl = request.form.get('ddl')
        if (not title or len(title) > 128) or (not ddl or len(ddl) > 128):
            flash('Invalid input.')
            return redirect(url_for('todolist'))  # 重定向回主页
        # 保存表单数据到数据库
        todo = Todo(title=title, ddl=ddl)
        db.session.add(todo)
        db.session.commit()
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('todolist'))  # 重定向回主页
    todos = Todo.query.all()
    return render_template('todolist.html', todos=todos)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movies(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        if not title or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit_movies', movie_id=movie_id))
        # 重定向回对应的编辑页面
        movie.title = title  # 更新标题
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('watchlist'))  # 重定向回主页
    return render_template('edit/edit_movies.html', movie=movie)  # 传入被编辑的电影记录


@app.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_books(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        if not title or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit_books', book_id=book_id))
        # 重定向回对应的编辑页面
        book.title = title  # 更新标题
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('readlist'))  # 重定向回主页
    return render_template('edit/edit_books.html', book=book)  # 传入被编辑的书籍记录


@app.route('/todo/edit/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def edit_todos(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        ddl = request.form['ddl']
        if (not title or len(title) > 60) or (not ddl or len(ddl) > 128):
            flash('Invalid input.')
            return redirect(url_for('edit_todos', todo_id=todo_id))
        # 重定向回对应的编辑页面
        todo.title = title  # 更新标题
        todo.ddl = ddl
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('todolist'))  # 重定向回主页
    return render_template('edit/edit_todos.html', todo=todo)  # 传入被编辑的书籍记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('watchlist'))  # 重定向回主页


@app.route('/book/delete/<int:book_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)  # 获取book记录
    db.session.delete(book)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('readlist'))  # 重定向回主页


@app.route('/todo/delete/<int:todo_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)  # 获取todo记录
    db.session.delete(todo)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('todolist'))  # 重定向回主页


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash("Successfully login!")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.")  # 若验证失败显示错误信息
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if (not username or len(username) > 20) or (not password or len(password) > 128):
            flash('Invalid input.')
            return redirect(url_for('settings'))
        # current_user.username = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        user = User.query.first()
        user.username = username
        user.set_password(password)
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


