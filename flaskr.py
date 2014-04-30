# All the imports
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import MySQLdb as mdb

# Create application
app = Flask(__name__)

# Load default config
app.config.update(dict(
	DEBUG = True,
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.from_object(__name__)
conn = mdb.connect('localhost','root','6WQti4T1','flaskr')

@app.route('/')
def show_entries():
	cursor = conn.cursor() 
	cursor.execute("SELECT title, text FROM entries ORDER BY id DESC")
	data = cursor.fetchall()
	return render_template('show_entries.html', entries=data)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	cursor = conn.cursor()
	cursor.execute('INSERT INTO entries (title,text) VALUES (%s, %s)', [request.form['title'], request.form['text']])
	conn.commit()
	flash('New entry was successfully posted!')
	return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in!')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out!')
	return redirect(url_for('show_entries'))

# Run application
if __name__ == "__main__":
	app.run(host='localhost')