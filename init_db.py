import sqlite3

conn = sqlite3.connect('database.db')

with open('db.sql') as f:
	conn.executescript(f.read())

# 创建一个执行句柄，执行后面的语句
cur = conn.cursor()

# 插入两条文章
cur.execute(
	'INSERT INTO posts(title, content) VALUES (?, ?)', ('Hello', 'World!')
)
cur.execute(
	'INSERT INTO posts(title, content) VALUES (?, ?)', ('你好', '世界!')
)

conn.commit()
conn.close()
