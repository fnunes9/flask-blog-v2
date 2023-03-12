import os
import psycopg2
from flask import Flask, render_template, request, url_for, flash, redirect


# cria a conexao com o BD
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="blog",
        user=os.getenv('DB_USERNAME'),
        password=os.environ['DB_PASSWORD']
    )
    return conn

# query todos os posts no banco
def get_post(post_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
    post = cur.fetchone()
    cur.close()
    conn.close()
    return post

# cria o serviço
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET_KEY_DEV')

# definicao das rotas
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts')
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        return render_template('404.html')
    return render_template('post.html', post=post)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO posts (title, content) VALUES (%s, %s)',
                         (title, content))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if post is None:
        return render_template('404.html')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('UPDATE posts SET title = %s, content = %s'
                         ' WHERE id = %s',
                         (title, content, id))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    if post is None:
        return render_template('404.html')
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM posts WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post[2]))
    return redirect(url_for('index'))

# inicia servico
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)