from flask import Flask, request, url_for, flash, redirect
from flask import render_template
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xiaobizhaizhi'

def get_db_conn():
	conn = sqlite3.connect('database.db')
	conn.row_factory = sqlite3.Row
	return conn


def get_post(post_id):
	conn = get_db_conn()
	post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
	return post


@app.route('/')  # 首页
def index():  # put application's code here
	conn = get_db_conn()
	posts = conn.execute('SELECT * FROM posts order by created desc').fetchall()
	return render_template('index.html', posts=posts)


@app.route('/posts/<int:post_id>')  # 获取文章
def post(post_id):
	post = get_post(post_id)
	return render_template('post.html', post=post)


@app.route('/posts/new', methods=['GET', 'POST'])  # 新增文章
def new():
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']

		if not title:
			flash('标题不能为空')
		elif not content:
			flash('内容不能为空')
		else:
			conn = get_db_conn()
			conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
			conn.commit()
			conn.close()
			flash("文章发布成功！")
			return redirect(url_for('index'))
	return render_template('new.html')


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])  # 编辑文章
def edit(post_id):
	post = get_post(post_id)
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']

		if not title:
			flash('标题不能为空')
		elif not content:
			flash('内容不能为空')
		else:
			conn = get_db_conn()
			conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
			conn.commit()
			conn.close()
			flash("文章更改成功！")
			return redirect(url_for('index'))
	return render_template('edit.html', post=post)


@app.route('/about')  # 关于
def about():
	return render_template('about.html')


if __name__ == '__main__':
	app.run()
