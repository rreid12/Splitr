import os 
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'splitr.db'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))
app.config.from_envvar('SPLITR_SETTINGS', silent=True)

'''TODO'''
#login_manager = LoginManager()
#login_manager.init_app(app)

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
            flash('You were logged in')
            return redirect(url_for('show_home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_home'))

@app.route('/')
def show_home():
	if session.get('logged_in'):
		db = get_db()
		cur = db.execute('select bill_id, bill_amount from bill order by bill_id asc')
		devices = cur.fetchall()
		return render_template('home.html', devices=devices)
	else:
		return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_device():
	error = None
	if not session.get('logged_in'):
		abort(401)
	roommates = int(request.form['contributors'])
	bill_amount = float(request.form['bill_amount'])
	result = split_bill(bill_amount, roommates)
	flash('Here is how you can split your bill:')
	return render_template('add.html', error=error, roommates=roommates, result=result, bill_amount=bill_amount)

def connect_db():
	"""Connects to the specific database"""
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
	"""Initialized database"""
	init_db()
	print('Initialized the database.')

def get_db():
	"""Opens a new database connection if there is none yet for the current application context"""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()

	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request"""
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.route('/clear', methods=['POST'])
def delete_all_devices():
	db = get_db()
	db.execute('delete from device')
	db.commit()
	flash('Devices cleared')
	return redirect(url_for('show_home'))

def split_bill(bill_amount, contributors):
	contributors = float(contributors)
	result = bill_amount / contributors
	print(result)
	db = get_db()
	db.execute('insert into bill (bill_amount, contributors, cost_per_contributor) values (?, ?, ?)',
		[bill_amount, contributors, result])
	db.commit()
	return result