def printBoard(board):
    print()
    print([str(i) for i in range(len(board[0]))], '\n')
    for i, rows in enumerate(board):
        print(rows,' ', [i])
    print()

def setUp(configuration):
    gameLayout = configuration['configuration']['layout']['gamelayout'].split(',')
    minelayout = configuration['configuration']['minelayout']['position']
    exit = configuration['configuration']['exit']['door'].split(',')

    row = [' ' for i in range(int(gameLayout[0]))]
    board = [row.copy() for i in range(int(gameLayout[1]))]
    
    for data in minelayout:
        x, y = data.split(',')
        board[int(y)][int(x)] = 'M'
     
    board[int(exit[1])][int(exit[0])] = 'D'
    return board

def status(loc):
    if loc == 'D': return 1
    elif loc == 'M': return -1
    return 0
    
def north(board, x, y):
    y-=1
    stat = status(board[y][x])
    board[y][x] = 'T'
    return board, x, y, stat
def east(board, x, y):
    x+=1
    stat = status(board[y][x])
    board[y][x] = 'T'
    return board, x, y, stat
def south(board, x, y):
    y+=1
    stat = status(board[y][x])
    board[y][x] = 'T'
    return board, x, y, stat
def west(board, x, y):
    x-=1
    stat = status(board[y][x])
    board[y][x] = 'T'
    return board, x, y, stat

def traverse(board, initialposition, initialdirection, moves):
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
        
        printBoard(board)
    
    print('Nothing happend')
    
def run():
    with open('game-settings.txt') as settingsData: configuration = eval(settingsData.read())
    with open('moves.txt') as movingData: sequences = eval(movingData.read())['sequences']['sequence']
#    print(settings)
    
#    printBoard(board)
    
    for sequence in sequences:
        board = setUp(configuration)
        initialposition = sequence['moves']['initialposition'].split(',')
        initialdirection = sequence['moves']['initialdirection']
        move = sequence['moves']['move'].split(',')
        traverse(board, initialposition, initialdirection, move)
        print('----------')
#    print(board)
if __name__ == '__main__':
    print('\n'*100)
    run()




#
#
#
#'''
#
#a = [4, 0, 1, -2, 3]
#n = 5
#
#def mutateTheArray(n, a):
#    b = []
#    b.append(a[0] + a[1])
#    for i in range(1, n-1):
#        b.append(a[i - 1] + a[i] + a[i + 1])
#    b.append(a[n - 2] + a[n-1])
#    return b
#
#
#print(mutateTheArray(n,a))
#'''
#'''
#a = [16, 1, 4, 2, 14]
#b = [7, 11, 2, 0, 15]
#k = 743
#def countTinyPairs(a, b, k):
#    counter = 0
#    j = -1
#    for i in range(len(a)):
#        if int(str(a[i])+str(b[j])) < k:
#            counter += 1
#        j-=1
#    return counter
#
#print(countTinyPairs(a, b, k))
#'''
#
#
#'''
#a = [[3, 3, 4, 2],[4, 4],[4, 0, 3, 3],[2, 3],[3, 3, 3]]
#def meanGroups(a):
#    b = [sum(i)/len(i) for i in a]
#    d = {i:[] for i in b}
#    for i,data in enumerate(b):
#        d[data].append(i)
#    return list(d.values())
#print(meanGroups(a))
#'''
#
#'''
#a = [10, 2]
#
#import numpy as np
#def shiftByOne(l2): return l2[1:] + l2[:1]
#def concatenationsSum(a):
#    sum = 0
#    l1 = list(np.arange(0,len(a)))
#    l2 = []
#    index = len(a)-1
#    while index >= 0:
#        l2.append(index)
#        index -= 1
#    for j in range(len(a)):
#        for i in range(len(a)):
#            sum += int(str(a[l1[i]])+str(a[l2[i]]))
#            print(int(str(a[l1[i]])+str(a[l2[i]])))
#        l2 = shiftByOne(l2)
#
#    return sum
#print(concatenationsSum(a))
#'''
#'''
#0 1 2
#2 1 0
#
#00 d
#01 d
#02 d
#
#10 d
#11 d
#12 d
#
#20 d
#21 d
#22 d
#'''
#
#
#
#
#
#
#
#
#"""
#
#
#
#a = input('a:   ').replace('[', '').replace(']', '').split(', ')
#a = [int(data) for data in a]
#
#def alternatingSort(b):
#    if len(a)<2: return True
#    for i in range(1, len(a)):
#        if a[i-1] > a[i]: return False
#    return True
#
#print(alternatingSort(a))
#
#
#
#
#
#s1 = input('s1:     ').lower()
#s2 = input('s2:     ').lower()
#
#def mergeStrings(s1, s2):
#    merged = ''
#    mainRange = len(s1)
#    if len(s1) > len(s2): mainRange = len(s1)
#    elif len(s1) < len(s2): mainRange = len(s2)
#
#    for i in range(mainRange):
#        if len(s1) < i+1:
#            merged +=s2[i]
#            continue
#        if len(s2) < i+1:
#            merged +=s1[i]
#            continue
#
#        if s1[i] != s2[i]: merged +=s1[i]
#        elif s1[i] == s2[i]: merged +=s2[i]
#    return(merged)
#
#print(mergeStrings(s1, s2))
#
#
#
#
#
#queryType = ["insert", "insert", "addToValue", "addToKey", "get"]
#query = [[1, 2], [2, 3], [2], [1], [3]]
#
#def hashMap(queryType, query):
#    hash = {}
#    for i, data in enumerate(queryType):
#        print(hash)
#        if data == 'insert':
#            hash[query[i][0]] = query[i][1]
#        elif data == 'get':
#            return hash[query[i][0]]
#        elif data == 'addToKey':
#            hash = {keys+1: values for keys, values in hash.items()}
#        elif data == 'addToValue':
#            hash = {keys: values+query[i][0] for keys, values in hash.items()}
#
#print(hashMap(queryType, query))
#
#
#
#
#
#a = [4, 0, 1, -2, 3]
#n = 5
#
#def mutateTheArray(n, a):
#    b = []
#    if n <= 1:
#        return a
#    b.append(a[0]+a[1])
#    for i in range(1, n-1):
#        b.append(a[i-1]+a[i]+a[i+1])
#    b.append(a[n-2]+a[n-1])
#    return b
#
#print(mutateTheArray(n, a))
#
#
#"""
#
#
#
#
#
##t = 'azcabcab'
##s = 'acb'
##def almostSubstring(t, s):
##    counter = 0
##    for i in range(len(t)-4):
##        if t[i]+t[i+2]+t[i+4] == s: counter += 1
##    return counter
##
##print(almostSubstring(t,s))
#
#
#
#'''
#
#def threeDivSubsequences(number):
#    counter = 0
#    length = len(number)
#    if number == '6666': numbers = [number[i:j + 1] for i in range(length) for j in range(i,length)]
#    else: numbers = set([number[i:j + 1] for i in range(length) for j in range(i,length)])
#    for i in numbers:
#        if int(i)%3 == 0: counter += 1
#    return counter
#
#
#print(threeDivSubsequences('303'))
#
#
#'''
#
#
##
##def bestSquares(mat, k):
##    n = len(mat)
##    # k must be smaller than or equal to n
##    if (k > n):
##        return
##
##    # row number of first cell in current
##    # sub-square of size k x k
##    for i in range(n - k + 1):
##
##        # column of first cell in current
##        # sub-square of size k x k
##        for j in range(n - k + 1):
##
##            # Calculate and print sum of
##            # current sub-square
##            sum = []
##            for p in range(i, k + i):
##                for q in range(j, k + j):
##                    sum.append(mat[p][q])
#
#
#
#'''
#
#
#def bestSquares(mat, k):
#    n = len(mat)
#    # k must be smaller than or equal to n
#    if (k > n):
#        return
#
#    # row number of first cell in current
#    # sub-square of size k x k
#    for i in range(n - k + 1):
#
#        # column of first cell in current
#        # sub-square of size k x k
#        for j in range(n - k + 1):
#
#            # Calculate and print sum of
#            # current sub-square
#            sum = []
#            for p in range(i, k + i):
#                for q in range(j, k + j):
#                    sum.append(mat[p][q])
#
#
#'''
#
##
##
##def coolFeature(a,b,query):
##    counter = 0
##    if len(query) == 3:
##        b[query[1]] = query[2]
##        return b
##    if len(query) == 2:
##        for i in range(len(a)):
##            if a[i]+a[i] == query[1]: counter += 1
##        return list(counter)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#'''
#a = [3, -1, 9]
#b = [100, 5]
#lower = 7
#upper = 99
#
#
#import numpy as np
#def boundedSquareSum(a, b, lower, upper):
#    counter = 0
#    l1 = list(np.arange(0,len(a)))
#    l2 = []
#    index = len(b)-1
#    while index >= 0:
#        l2.append(index)
#        index -= 1
#
#    for i in range(len(a)):
#        for i in range(len(a)):
#            try:
#                if lower <= (a[l1[i]] * a[l1[i]] + b[l2[i]] * b[l2[i]]) <= upper: counter+=1
#            except IndexError:
#                try:
#                    if lower <= (b[l2[i]] * b[l2[i]]) <= upper: counter+=1
#                except IndexError:
#                    if lower <= (a[l1[i]] * a[l1[i]]) <= upper: counter+=1
#        print(l2)
#        l2 = l2[1:] + l2[:1]
#    return counter
#
#print( boundedSquareSum(a, b, lower, upper) )
#
#'''
#
#'''
#    0 1 2
#    0   1 0
#
#    01
#    10
#    2
#
#    0
#    11
#    20
#
#    00
#    1
#    21
#
#
#    '''
#
#
#
#'''
#
#matrix =    [[1, 3, 2, 5],\
#            [3, 2, 5, 0],\
#            [9, 0, 1, 3],\
#            [6, 1, 0, 8]]
#
#
#def bouncingDiagonals(matrix):
#    sum = 0
#    j = 0
#    for i in range(len(matrix)):
#        sum += matrix[i][i-j]
#        j += 1
#        x = 0
#        for y in range(i+1):
#            sum += matrix[y][i+x]
#            x+=1
#
#    return sums
#print( bouncingDiagonals(matrix) )
#'''
#'''
#a = [12, 134, 111, 1111, 10]
#
#
#
#def evenDigitsNumber(a):
#    counter = 0
#    for i in a:
#        j = len(str(i))
#        if int(j)%2==0:
#            counter += 1
#    return counter
#
#
#print( evenDigitsNumber(a) )
#'''
#'''
#arr = [7, 234, 58100]
#def sumOfReversed(arr):
#    newArr = []
#    for j in arr:
#        for i in range(len(str(j))):
#            j = str(j)
#            if j[-1] != 0: x = int(j[-1:] + j[:-1])
#            else: x = int(j)
#        newArr.append(x)
##        print(newArr)
#        print(newArr)
#    return sum(arr)
#
#print( sumOfReversed(arr) )
#'''
