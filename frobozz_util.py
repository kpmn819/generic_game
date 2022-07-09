

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
