from flask import current_app, g
from flask.cli import with_appcontext

import click
import pickle

class TodoItem:
	def __init__(self, content, itemid):
		self.itemid = itemid
		self.content = content
		self.completed = False

class TodoList():
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.__items = list()
		
	
	def add_item(self, content):
		self.__items.append(TodoItem(content, len(self.__items)+1))
	
	def remove_item(self, key):
		if type(key) == int:
			for item in self.__items:
				if item.itemid == key:
					del item
				else:
					raise KeyError('Item does not exist')

		else:
			raise TypeError('Key must be an integer')

	def __str__(self) -> str:
		return str(self.__items)

	
	def find_item(self, key):
		if type(key) == int:
			for item in self.__items:
				if item.itemid == key:
					return item
				else:
					raise KeyError('Item does not exist')

		else:
			raise TypeError('Key must be an integer')
	
	def as_dict(self):
		return {'id': self.id, 'name': self.name}
	
	def __len__(self):
		return len(self.__items)
	
	def as_list(self):
		return self.__items



class AllTodos():
	'''
	TO BE USED AS A SINGLETON ONLY
	Do not instantiate this class. Instead, use the returned object from the get_todos() method
	'''
	def __init__(self):

		self.length = 0
		self.__items = list()
	
	def append(self, todo):
		if type(todo) != TodoList:
			raise TypeError('Object only supports arguments of type \'TodoList\'')
		
		self.__items.append(todo)
		self.length += 1
	
	def find(self, id):
		for todo in self.__items:
			if todo.id == id:
				return todo
		
		return None
	
	def findbyname(self, name):
		for todo in self.__items:
			if todo.name == name:
				return todo
		
		return None

	def store_new(self, name):
		lis = TodoList(self.length+1, name)

		self.append(lis)
		self.length += 1

		return lis
	





def get_todos():
	if not 'todos' in g:
		with open(current_app.config['LISTDATA'], 'rb') as f:
			g.todos = pickle.load(f)
	
	return g.todos

def close_todos(e):
	g.pop('todos', None)

def init_todos():
	todos_list = AllTodos() # The only place it should ever be instantiated
	
	file = open(current_app.config['LISTDATA'], 'wb')
	pickle.dump(todos_list, file)
	file.close()

def commit_todos():
	todos_list = get_todos()

	file = open(current_app.config['LISTDATA'], 'wb')
	pickle.dump(todos_list, file)
	file.close()

@click.command('init-todos')
@with_appcontext
def init_todos_command():
	init_todos()
	click.echo('Todos initialised!')

def init_app(app):
	app.teardown_appcontext(close_todos)
	app.cli.add_command(init_todos_command)
