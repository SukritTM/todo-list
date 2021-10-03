from flask import Blueprint, g, render_template, request, session, url_for
from werkzeug.utils import redirect
from app.auth import login_required

from app.db import get_db
from app.todo import *

bp = Blueprint('pages', __name__, url_prefix='/')


@bp.route('/home', methods = ['GET'])
@login_required
def home():
	if request.method == 'GET':
		db = get_db()
		todos = get_todos()


		userid = g.user['uid']

		todoids = db.execute(
			'''
			SELECT tid
			FROM user u INNER JOIN todo t
			ON u.uid = t.uid
			WHERE tid = ?
			''',
			(userid,)
		).fetchall()

		todolists = []
		for id in todoids:
			todolists.append(todos.find(id[0]).as_dict())
		
		return render_template('pages/home.html', todolists = todolists)

@bp.route('/todo/<int:tid>', methods = ('GET',))
@login_required
def todo(tid):
	uid = g.user['uid']

	belongs = get_db().execute(
		'''SELECT * FROM todo WHERE tid = ? AND uid = ?''',
		(tid, uid)
	).fetchone()

	if not belongs:
		return '', 403
	
	todolist = get_todos().find(tid)

	return render_template('pages/todo.html', todolist = todolist)