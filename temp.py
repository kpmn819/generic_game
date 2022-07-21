'''class MyClass:
    def __init__(self, name):
        self.name = name
        self.pretty_print_name()
        print(self)

    def pretty_print_name(self):
        print("This object's name is {}.".format(self.name))

my_objects = {}
for i in range(1,6):
    name = 'button{}'.format(i)
    my_objects[name] = my_objects.get(name, MyClass(name = name))'''

button_list = [[1, False, 3, True], [4, True, 6, True] ,[7, False, 9, True]]
class Button():
 def __init__(self,in_port, in_stat, out_port, out_stat):
        self.in_port = in_port
        self.in_stat = in_stat
        self.out_port = out_port
        self.out_stat = out_stat
def something():
    x = 'something'
    print(x)
    def nextthing():
        print('not working')


button_list = [Button(x, y, z, q) for x, y, z, q in button_list]
button_list[0].in_port = 99
print(button_list[0].in_port)
something()

