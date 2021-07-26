import sys
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def printBoard(board):
    print()
    print([str(i) for i in range(len(board[0]))], '\n')
    for i, rows in enumerate(board):
        print(rows,' ', [i])
    print()
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def setUp(configuration):
    gameLayout = configuration['configuration']['layout']['gamelayout'].split(',')
    minelayout = configuration['configuration']['minelayout']['position']
    exit = configuration['configuration']['exit']['door'].split(',')
    try:
        row = [' ' for i in range(int(gameLayout[0]))]
        board = [row.copy() for i in range(int(gameLayout[1]))]
        for data in minelayout:
            x, y = data.split(',')
            board[int(y)][int(x)] = 'M'
        board[int(exit[1])][int(exit[0])] = 'D'
    except IndexError:
        print('One or more of the inputs are out of bound, check game-settings.txt')
        sys.exit()
    return board
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def status(loc):
    if loc == 'D': return 1
    elif loc == 'M': return -1
    return 0
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def north(board, x, y):
    y-=1
    stat = status(board[y][x])
    board[y][x] = 'T'
    return board, x, y, stat
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def east(board, x, y):
    x+=1
    stat = status(board[y][x])
    board[y][x] = 'T'
    return board, x, y, stat
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def south(board, x, y):
    y+=1
    stat = status(board[y][x])
    board[y][x] = 'T'
    return board, x, y, stat
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def west(board, x, y):
    x-=1
    stat = status(board[y][x])
    board[y][x] = 'T'
    return board, x, y, stat
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def traverse(board, initialposition, initialdirection, moves, chart=False):
    x, y = initialposition
    x = int(x)
    y = int(y)
    if board[y][x] == 'D':
        print('Success')
        return
    elif board[y][x] == 'M':
        print('Mine hit')
        return
    try: board[y][x] = 'S'
    except IndexError:
        print('Out of bounds')
        return
    directions = ['north','east','south','west']
    directionFunctions = [north,east,south,west]
    direction = directions.index(initialdirection.lower())
    for index, move in enumerate(moves):
        if chart: printBoard(board)
        index += 1
        if not(0 < x < len(board[0])) or not(0 < y < len(board)):
            print(index, 'Out of bounds')
            return
        try:
            if move == 'm':
                board, x, y, stat = directionFunctions[direction](board, x, y)
            elif move == 'r':
                if direction+1 == len(directions): direction = 0
                else: direction+=1
        except IndexError:
            print(index, 'Out of bounds')
            return
        if stat == 1:
            print(index, 'Success')
            return
        elif stat == -1:
            print(index, 'Mine hit')
            return
        elif stat == 0 and index != len(moves):
            print(index, 'Still in danger')
    print('Nothing happend')
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def run():
    with open('game-settings.txt') as settingsData: configuration = eval(settingsData.read())
    with open('moves.txt') as movingData: sequences = eval(movingData.read())['sequences']['sequence']
    for sequence in sequences:
        board = setUp(configuration)
        initialposition = sequence['moves']['initialposition'].split(',')
        initialdirection = sequence['moves']['initialdirection']
        move = sequence['moves']['move'].split(',')
        traverse(board, initialposition, initialdirection, move, chart=True)
        print('- '*25)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
if __name__ == '__main__':
    print('\n'*100)
    run()






