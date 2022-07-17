
class Something():
	def __init__(self, somevar):
		self.somevar = somevar
	def print_added(self, another):
		print(another)


zow = Something('42')
print(zow.somevar)
zow.another = '99'
print(zow.another)
Something.print_added(zow,zow.another)