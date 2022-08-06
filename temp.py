import generic_game

def blit_formatted(file)
    # reads text formatted as Text, Size, X Postion or 'center', Y Position, Color
    lines = get_file('free_cash.csv',5)[0]
    for index, line in enumerate(lines):
        print(line[0])
        if line[2] == 'center':
            line[2] = image_centerx
        print(line[2])
        greeting = line[0]
        greet = TextObject(greeting, (line[2], line[3]), line[1], line[4] )
        TextObject.font_process(greet)