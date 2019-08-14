import sys
import random

def must_be_positive(num):
    if num <= 0:
        raise ValueError(num)

def is_valid_int(integer):
  """
  checks to see if number represents a valid integer
  @number: a string that might represent an integer
  @returns: true if the string represents an integer
  """
  integer = integer.strip()
  if len(integer) == 0:
    return False
  else:
    return (integer.isdigit() or #only digits
            #or a negative sign followed by digits
            (integer.startswith('-') and integer[1:].isdigit()))

def is_valid_move(move,ai_board,width,height):
    move = move.split()

    if len(move) != 2:
        return False

    (row,col) = move #get row row and column

    if not is_valid_int(row):#row isn't a number
        return False

    if not is_valid_int(col):#column isn't a number
        return False

    #safe to convert to integers
    row = int(row)
    col = int(col)

    if row not in range(height) or col not in range(width): #move needs to be on the board
        return False

    if ai_board[row][col] != '*': #we can't play at a place that's already been played
        return False

    return True #move wasn't illegal so it must be legal
    
def get_seed():
    while True:
        try:
            seed = int(input('Enter the seed: '))
            return seed
        except ValueError:
            pass

def get_width():
    while True:
        try:
            width = int(input('Enter the width of the board: '))
            must_be_positive(width)
            return width
        except ValueError:
            pass

def get_height():
    while True:
        try:
            height = int(input('Enter the height of the board: '))
            must_be_positive(height)
            return height
        except ValueError:
            pass

def get_file():
    file = input('Enter the name of the file containing your ship placements: ')

    with open(file) as ships:
        contents = ships.readlines()    

    return contents

def get_AI():
    while True:
        try:
            AI = int(input('Choose your AI.\n'
                       '1. Random\n'
                       '2. Smart\n'
                       '3. Cheater\n'
                       'Your choice: '))
            must_be_positive(AI)
            if AI > 3:
                raise ValueError(AI)
            return AI
        except ValueError:
            pass

def unfired_shots(width,height):
    unfired_places = []
    for row in range(height):
        for col in range(width):
            unfired_places.append([row,col])
    return unfired_places

def is_right_placement(contents,width,height):
    ship_coords = []
    symbols = []
    row = []
    col = []
    ship_dict = {}
    
    for content in contents:
        content = content.split()
        ship_coords.append(content[1:-1])
        symbols.append(content[0])
        row.append(content[1:-1:2])
        col.append(content[2::2])
        ship_dict[content[0]] = content[1:] 

    for symbol in symbols:
        if symbols.count(symbol) > 1:
            sys.exit(0)

    for symbol, coords in ship_dict.items():
        for number in coords:
            if '-' in number:
                print('Error %s is placed outside of board. Terminating game.'
                      % symbol)
                sys.exit(0)
            elif int(number) > width or int(number) > height:
                print('Error %s is placed outside of board. Terminating game.'
                      % symbol)
                sys.exit(0)
                
    for row,col in zip(row,col):
        if row[0] != row[1] and col[0] != col[1]:
            print('Ships cannot be placed diagonally. Terminating game.')
            sys.exit(0)
            
    return ship_dict
    
            
    
def make_board(width,height):
    board = []
    for row_index in range(height):
        row = ['*'] * width
        board.append(row)

    return board

def place_user_ships(board,ships):
    rows = []
    cols = []
    for coords in ships.values():
        rows.append(coords[1:-1:2])
        cols.append(coords[2::2])
        
    print('Placing ship from %s, %s to %s, %s.'
          % (min(rows[0]),min(cols[0]),max(rows[0]),max(cols[0])))
    
    for name, coords in ships.items():
        if (int(coords[0]) == 0 and int(coords[2]) == 0 and
            int(coords[1]) == 0 and int(coords[3]) == 0):
            board[int(coords[0])][int(coords[2])] = name
        elif coords[0] == coords[2]:
            if int(coords[1]) > int(coords[3]):
                length = int(coords[1]) - int(coords[3]) + 1
                board[int(coords[0])][int(coords[1])] = name
                for num in range(length):
                    board[int(coords[0])][int(coords[1])-num] = name
            elif int(coords[3]) > int(coords[1]):
                length = int(coords[3]) - int(coords[1]) + 1
                board[int(coords[0])][int(coords[1])] = name
                for num in range(length):
                    board[int(coords[0])][int(coords[3])-num] = name
        elif coords[1] == coords[3]:
            if int(coords[0]) > int(coords[2]):
                length = int(coords[0]) - int(coords[2]) + 1
                board[int(coords[0])][int(coords[1])] = name
                for num in range(length):
                    board[int(coords[0])-num][int(coords[1])] = name
            elif coords[2] > coords[0]:
                length = int(coords[2]) - int(coords[0]) + 1
                board[int(coords[0])][int(coords[1])] = name
                for num in range(length):
                    board[int(coords[2])-num][int(coords[1])] = name
    return board

def place_AI_ships(board,ships,width,height):
    lengths = {}
    where_AI = {}
    for name,coords in ships.items():
        if (int(coords[0]) == 0 and int(coords[2]) == 0 and
            int(coords[1]) == 0 and int(coords[3]) == 0):
            lengths[name] = 1
        elif coords[0] == coords[2]:#if horz
            if int(coords[1]) > int(coords[3]):
                length_ship = int(coords[1]) - int(coords[3]) + 1
                lengths[name] = length_ship
            elif coords[3] > coords[1]:
                length_ship = int(coords[3]) - int(coords[1]) + 1
                lengths[name] = length_ship
        elif coords[1] == coords[3]:
            if int(coords[0]) > int(coords[2]):
                length_ship = int(coords[0]) - int(coords[2]) + 1
                lengths[name] = length_ship
            elif coords[2] > coords[0]:
                length_ship = int(coords[2]) - int(coords[0]) + 1
                lengths[name] = length_ship

    for name,length in lengths.items():
        direction = random.choice(['vert','horz'])
        if direction == 'horz':
            if width == 1 and height == 1:
                row = random.randint(0,0)
                col = random.randint(0,0)
                where_AI[name] = [row,col]
                board[row][col] = name
            else:
                row = random.randint(0,height-1)
                col = random.randint(0,width - length)
                where_AI[name] = [row,col]
                for num in range(length):
                    board[row][col+num] = name
                
        elif direction == 'vert':
            if width == 1 and length == 1:
                row = random.randint(0,0)
                col = random.randint(0,0)
                where_AI[name] = [row,col]
                board[row][col] = name
            else:
                row = random.randint(0,height-length)
                col = random.randint(0,width)
                where_AI[name] = [row,col]
                for num in range(length):
                    board[row+num][col] = name
    return board
                
def scan_board(board):
    print('Scanning Board')
    print(' ', end = '') #display some white space for alignment purposes
    #display the column headers
    for col_num in range(len(board[0])):
        print('', col_num, end = '')
    print()

    for (row_num,row) in enumerate(board): #for each row
        if row != '*':
            row = '*' * len(row)
            print(row_num, ' '.join(row))
        else:
            print(row_num, ' '.join(row)) #print it out the row header and each element with | in between
    print()
    return

def display_board(board):
    print('My Board')
    print(' ', end = '') #display some white space for alignment purposes
    #display the column headers
    for col_num in range(len(board[0])):
        print('', col_num, end = '')
    print()

    for (row_num,row) in enumerate(board): #for each row
        print(row_num, ' '.join(row)) #print it out the row header and each element with | in between

    return

def get_move(player,ai,user_board,ai_board,width,height,unfired_places):
    move = ''
    if player == 'user':
        scan_board(ai_board)
        display_board(user_board)
        while not is_valid_move(move,ai_board,width,height):
            move = input('Enter row and column to fire on separated by a space: ')

        (row,col) = move.split()

        row = int(row)
        col = int(col)

        return (row,col)

    elif player == 'AI':
        if ai == 1:
            return random_ai(unfired_places)
        elif ai == 2:
            smart_ai()
        elif ai == 3:
            cheater_ai()

def random_ai(unfired_places):
    fires = random.choice(unfired_places)
    return fires

def smart_ai():
    pass#WORK ON

def cheater_ai():
    pass#WORK ON

def make_move(player,move,user_board,ai_board,ships):
    (row,col) = move
    if player == 'user':
        if ai_board[row][col] in ships:
            ai_board[row][col] = 'X'
            print('Hit!')
        else:
            ai_board[row][col] = '0'
            print('Miss!')
    else:
        print('The AI fires at location (%d,%d)' % (row,col))
        if user_board[row][col] in ships:
            user_board[row][col] = 'X'
            print('Hit!')
        else:
            user_board[row][col] = 'O'
            print('Miss!')

def is_gameover(user_board,AI_board):
    return False#WORK ON

def play_battleship():

    unfired_places = []
    places_hit = []
    ships = {}
    lengths = {}
    symbols = []
    hit = 'X'
    miss = '0'
    players = ['user','AI']
    
    seed = get_seed()
    width = int(get_width())
    height = int(get_height())
    file_contents = get_file()
    AI = get_AI()
    unfired_places = unfired_shots(width,height)

    ships = is_right_placement(file_contents,width,height)
    for name in ships:
        symbols.append(name)

    print(ships)
    random.seed(seed)
    my_board = make_board(width,height)
    AI_board = make_board(width,height)
    
    my_ships = place_user_ships(my_board,ships)
    AI_ships = place_AI_ships(AI_board,ships,width,height)
    turn = random.randint(0,1)

    while not is_gameover(my_board,AI_board):
        move = get_move(players[turn],AI,my_ships,AI_ships,width,height,unfired_places)
        make_move(players[turn],move,my_ships,AI_ships,symbols)
        turn = (turn+1)%2



play_battleship()
