from flask import Blueprint, g, render_template, request, session, flash
from flask.helpers import url_for

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from app.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods = ('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		confirm = request.form['confirm']
		db = get_db()

		error = None
		if not username:
			error = 'Username required'
		elif not password:
			error = 'password required'
		elif password != confirm:
			error = 'passwords do not match'
		
		if not error:
			hashed = generate_password_hash(password)
			try:
				db.execute(
					"INSERT INTO user (uname, pass) values (?, ?)",
					[username, hashed]
				)
				db.commit()
			except db.IntegrityError:
				error = "Username is taken"
			else:
				return redirect(url_for('auth.login'))

		if error:
			flash(error)
			return render_template('auth/register.html')

	else:
		return render_template('auth/register.html')


@bp.route('/login', methods = ('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()

		user = db.execute(
			"SELECT * FROM user WHERE uname = ?",
			(username,)
		).fetchone()
		
		error = None
		if not user:
			error = 'Username is incorrect'
		elif not check_password_hash(user['pass'], password):
			error = 'password is incorrect'

		if error is None:
			session.clear()
			session['user-id'] = user['uid']
		
		else:
			flash(error)
			return render_template('auth/login.html')

		# return redirect(url_for('mainpage.home'))
		flash('Logged in!')
		return render_template('auth/login.html')
	
	else:
		return render_template('auth/login.html')


bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('auth.login'))


# Wrapper to ensure login
def login_required(func):
	def wrap(*args, **kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))
		return func(*args, **kwargs)
	
	return wrap