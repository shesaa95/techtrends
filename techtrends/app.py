import sqlite3
import logging
import datetime
import sys
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort


# Adding a global variable for db_connection_count
db_connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info('Article not found')
      return render_template('404.html'), 404
    else:
      
      app.logger.info('{date}, Article \"{article}\" retrieved!'.format(date=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), article=post[2]))
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About Page Request Successful')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            
            app.logger.info('{date}, Article \"{article}\" created!'.format(date=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), article=title))
            return redirect(url_for('index'))

    return render_template('create.html')

# added /healthz endpoint
@app.route('/healthz')
def healthz():
    response = app.response_class(
        response=json.dumps({"result":"OK - healthy"}),
        status=200,
        mimetype='application/json'
    )
    return response

# added /metrics endpoint
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    count = connection.execute('SELECT COUNT(*) FROM posts')
    count_list = str(count.fetchone()[0])
    connection.close()

    response = app.response_class(
        response=json.dumps({"db_connection_count": db_connection_count, "post_count": count_list}),
        status=200,
        mimetype='application/json'
    )
    return response

    

# start the application on port 3111
if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
        filename='app.log',
        filemode='w')        

    console_stdout_handler = logging.StreamHandler(sys.stdout)
    console_stderr_handler = logging.StreamHandler(sys.stderr)
    console_stdout_handler.setLevel(logging.DEBUG)
    console_stderr_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console_stdout_handler.setFormatter(formatter)
    console_stderr_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(console_stdout_handler)
    logging.getLogger('').addHandler(console_stderr_handler)



    app.run(host='0.0.0.0', port='3111')
