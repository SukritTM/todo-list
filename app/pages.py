from flask import Blueprint, g, render_template, request, session, url_for
from werkzeug.utils import redirect
from app.auth import login_required

from app.db import get_db
from app.todo import *

bp = Blueprint('pages', __name__, url_prefix='/')


@bp.route('/home', methods = ('GET', 'POST'))
@login_required
def home():
	
	db = get_db()
	todolists = get_todos()

	userid = g.user['uid']

	
	if request.method == 'POST':
		listid = todolists.store_new(request.form['name']).id	
		db.execute(
			'INSERT INTO todo VALUES (?, ?)',
			(str(listid), str(userid))
		)
		db.commit()
		commit_todos()

	
		

	todoids = db.execute(
		'''
		SELECT tid
		FROM user u INNER JOIN todo t
		ON u.uid = t.uid
		WHERE t.uid = ?
		''',
		(userid,)
	).fetchall()

	tododictlist = []
	for id in todoids:
		tododictlist.append(todolists.find(id[0]).as_dict())
	
	print(todoids)
	
	
	
	return render_template('pages/home.html', todolists = tododictlist)

@bp.route('/todo/<int:tid>', methods = ('GET', 'POST'))
@login_required
def todo(tid):

	uid = g.user['uid']

	belongs = get_db().execute(
		'''SELECT * FROM todo WHERE tid = ? AND uid = ?''',
		(tid, uid)
	).fetchone()

	if not belongs:
		return '', 403

	todolists = get_todos()

	todolist = todolists.find(tid)

	if request.method == 'POST':
		todolist.add_item(request.form['add'])
		
		commit_todos()


	return render_template('pages/todo.html', todolist = todolist.as_list())