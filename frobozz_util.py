
#======== class example ==========
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
#\\\\\\\\\ class example \\\\\\\\\\\\\\\
# ///////////// CREATE CLASS INSTANCES FROM LIST //////////
class Button():
 def __init__(self,in_port, in_stat, out_port, out_stat):
        self.in_port = in_port
        self.in_stat = in_stat
        self.out_port = out_port
        self.out_stat = out_stat

button_list = [[1, False, 3, True], [4, True, 6, True] ,[7, False, 9, True]]

button_list = [Button(x, y, z, q) for x, y, z, q in button_list]
button_list[0].in_port = 99
print(button_list[0].in_port)
#\\\\\\\\\\\\\ CLASS INSTANCES \\\\\\\\\\\\\\\\\\\
# ///////////// ENUMERATE EXAMPLE ///////////////////
users = ["Test User", "Real User 1", "Real User 2"]
for index, user in enumerate(users):
    if index == 0:
        print("Extra verbose output for:", user)
    print(user)
# \\\\\\\\\\\\\ ENUMERATE EXAMPLE \\\\\\\\\\\\\\\\\\

#///////////////// CSV FILE READER /////////////////
def get_file(list_file, col_count):
    # now a more generic reader that can take any number of columns
    global row_count
    global file_error
    try:
        ''' call with file and get back list of lists'''
        with open(list_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            rowlist = []
            cvs_list = []
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    # avoids the header line
                    rowlist = [row[0]] # initalizes the list first item
                    if col_count > 1:
                        for x in range(1,col_count):
                            rowlist.append(row[x])
                        
                    cvs_list.append(rowlist)
                    # this is a 0 based list of lists
                    # access questions_list[q# - 1][column]
                line_count += 1
            #print(f'Processed {line_count} lines.')
            row_count = line_count - 1
            # returns lists within lists acces via [list of items][items]
            return [cvs_list]
    except FileNotFoundError:
        print('file not found')
        # print message on screen
        file_error = True
# \\\\\\\\\\\\\\\\\\\\\\\\ CSV FILE READER \\\\\\\\\\\\\\\\\\\\\\\\\\\

# /////////////////// BREAK UP A LIST INTO A BUNCH OF LISTS /////////////
# Split a Python List into Chunks using For Loops
our_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
chunked_list = list()
chunk_size = 3
for i in range(0, len(our_list), chunk_size):
    chunked_list.append(our_list[i:i+chunk_size])
print(chunked_list)
#////////////////////// or this ///////////////////
# Split a Python List into Chunks using list comprehensions
our_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
chunk_size = 3
chunked_list = [our_list[i:i+chunk_size] for i in range(0, len(our_list), chunk_size)]
print(chunked_list)

# /////////////////////////////// class + inheritence + caller /////////////////////////
class ScreenObject():
    def __init__(self, location):
        
        self.location = location    
        
class TextObject(ScreenObject):
    def __init__(self, text, location, size, color, width=None, font=None):
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.width = width
        super().__init__(location)

    def parse_string(self, text, width):
        print('parse string has' + text + ' '+ str(width))
        # this handy util breaks up long lines for us
        lines_list = textwrap.wrap(text, width)
        
	# will return any number of lines of final_length
        return lines_list 

stuff ='here is a really long line that will have to be compressed by our formatter'
zow = TextObject(stuff, (200,300), 50, red)
print(zow.color)
zow.text =TextObject.parse_string(zow, stuff, 10)
print(zow.text)
# ///////////////////////////////////////////////////    
