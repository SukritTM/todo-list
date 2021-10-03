from flask import Flask

import os

from app.db import init_db_command


def create_app():
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY = 'dev',
		DATABASE = os.path.join(app.instance_path, 'users.sqlite'),
		LISTDATA = os.path.join(app.instance_path, 'todos.pickle')
	)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import db
	db.init_app(app)

	from . import todo
	todo.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import pages
	app.register_blueprint(pages.bp) 

	@app.route('/')
	def say_hello():
		return '<h1>hello world</h1>'

	return app