from flask import Flask

import os

from app.db import init_db_command


def create_app():
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY = 'dev',
		DATABASE = os.path.join(app.instance_path, 'users.sqlite')
	)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import db
	db.init_app(app)

	@app.route('/')
	def say_hello():
		return '<h1>hello world</h1>'

	return app