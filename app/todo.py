class TodoItem:
	def __init__(self, content, itemid):
		self.itemid = itemid
		self.content = content
		self.completed = False

class TodoList:
	def __init__(self, user):
		self.uid = user
		self.todo = []
	
	def add_item(self, content):
		self.todo.append(TodoItem(content, len(self.todo)+1))
	
	def remove_item(self, key):
		if type(key) == int:
			for item in self.todo:
				if item.itemid == key:
					del item
				else:
					raise KeyError('Item does not exist')

		else:
			raise TypeError('Key must be an integer')
	
	def find_item(self, key):
		if type(key) == int:
			for item in self.todo:
				if item.itemid == key:
					return item
				else:
					raise KeyError('Item does not exist')

		else:
			raise TypeError('Key must be an integer')