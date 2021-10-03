from flask import current_app, g
from flask.cli import with_appcontext

import click
import pickle

class TodoItem:
	def __init__(self, content, itemid):
		self.itemid = itemid
		self.content = content
		self.completed = False

class TodoList(list):
	def __init__(self, id, name):
		self.id = id
		self.name = name
		
	
	def add_item(self, content):
		self.append(TodoItem(content, len(self.todo)+1))
	
	def remove_item(self, key):
		if type(key) == int:
			for item in self:
				if item.itemid == key:
					del item
				else:
					raise KeyError('Item does not exist')

		else:
			raise TypeError('Key must be an integer')
	
	def find_item(self, key):
		if type(key) == int:
			for item in self:
				if item.itemid == key:
					return item
				else:
					raise KeyError('Item does not exist')

		else:
			raise TypeError('Key must be an integer')
	
	def as_dict(self):
		return {'id': self.id, 'name': self.name}

# unused rn
class AllTodos(list):
	'''
	TO BE USED AS A SINGLETON ONLY
	Do not instantiate this class. Instead, use the returned object from the get_todos() method
	'''
	def __init__(self):
		super().__init__()

		length = 0
	
	def append(self, todo):
		if type(todo) != TodoList:
			raise TypeError('Object only supports arguments of type \'TodoList\'')
		
		super().append(todo)
	
	def find(self, id):
		for todo in self:
			if todo.id == id:
				return todo
		
		return None
	
	def store_new(self, name):
		lis = TodoList(len(self), name)

		self.append(lis)
	



def get_todos():
	if not 'todos' in g:
		with open(current_app.config['LISTDATA'], 'rb') as f:
			g.todos = pickle.load(f)
	
	return g.todos

def close_todos(e):
	g.pop('todos', None)

def init_todos():
	todos_list = AllTodos() # The only place it should ever be instantiated
	todos_list.append(TodoList(1, 'list1'))
	todos_list[0].add_item('Todolist')
	
	file = open(current_app.config['LISTDATA'], 'wb')
	pickle.dump(todos_list, file)
	file.close()

def commit_todos(e):
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
	app.teardown_appcontext(commit_todos)
	app.teardown_appcontext(close_todos)
	app.cli.add_command(init_todos_command)
