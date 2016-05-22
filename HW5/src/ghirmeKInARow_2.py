''' ghirmeKInARow.py
Eden Ghirmai 
CSE415 Spr16 - 5/9/2015
Assignment 5: Game-Playing Agents
'''

import random

__current_state = None 
__k = 0 
__side = None
__opponent = None
__rows = 0
__columns = 0 
__winning_possible = {}
__forbidden = []
__zArray = []
__players_amt = 2

def introduce():
    'Returns introduction to the AI playing k-in-a-row'
    return "Hi, I am Beyonce and I am a master k-in-a-row player created by Eden Ghirmai (ghirme@uw.edu). I am a diva and I am gonna winnnnn"

def nickname():
    'Returns the nickname of the AI'
    return "Queen B"

def prepare(initial_state, k, what_side_I_play, opponent_nickname): 
    global __current_state, __k, __opponent, __rows, __columns, __winning_possible, __side
    #set initial variables
    __current_state = initial_state[0] 
    __rows = len(__current_state)
    __columns = len(__current_state[0])

    __k = k 
    __side = what_side_I_play
    __opponent = opponent_nickname

    #initalize zobrist transpotition table
    init_zobrist()

    # find possible winning squares 
    update_available()                    

    return "OK"

def makeMove(currentState, currentRemark, timeLimit=10000):
    global __side, __current_state, __columns, __rows, __winning_possible
    
    update_available()

    __current_state = currentState[0]
    for row in range(__rows):
        for column in range(__columns):
            square = __current_state[row][column]
            if canWin((row, column)) and square == ' ':
                __current_state[row][column] = __side
                resultState = [__current_state, otherSide()]
                return [[(row, column), resultState], "hehehe I'm going to win"]


def otherSide():
    global __side

    if __side == 'X':
        return 'O'

    if __side == 'O':
        return 'X'


def canWin(square):
    global __winning_possible

    if square in __winning_possible["l_diag"] or square in __winning_possible["r_diag"] or square in __winning_possible["rows"] or square in __winning_possible["column"]:
        return True

def staticEval(state):
    return

def init_zobrist():
    'initializes the state using zobrist method of initializing and randomizing'
    global __zArray, __rows, __columns, __players_amt
    __zArray = [[[0 for k in range(2)] for j in range(__columns)] for i in range(__rows)]

    for row in range(__rows):
        for column in range(__columns):
            for player in range(__players_amt):
                __zArray[row][column][player] = random.getrandbits(64)        


def update_available():
    global __current_state, __rows, __columns, __winning_possible, __k
    k = __k
    __winning_possible["l_diag"] = []
    __winning_possible["r_diag"] = []
    __winning_possible["column"] = []
    __winning_possible["rows"]   = []    
    #check rows 
    for row in range(__rows):
        current = []
        for column in range(__columns):
            square = __current_state[row][column]
            if square == ' ' or square == __side:
                current.append((row, column))
            else:
                if len(current) >= k:
                    __winning_possible["rows"] += current 
                    current = []
        if len(current) >= k:
            __winning_possible["rows"] += current 
            current = []                            

    #check columns 
    for column in range(__columns):
        current = []
        for row in range(__rows): 
            square = __current_state[row][column]
            if square == ' ' or square == __side:
                current.append((row, column))
            else:
                if len(current) >= k:
                    __winning_possible["column"] += current
                    current = []
        if len(current) >= k:
            __winning_possible["column"] += current
            current = []                    

    #check left diag
    for row in range(__rows):
        column = 0
        current = []
        while row < __rows and column < __columns:
            square = __current_state[row][column]
            if square == ' ' or square == __side:
                current.append((row, column))
            else:           
                if len(current) >= k:
                    __winning_possible["l_diag"] += current
                    current = []
            row += 1
            column += 1
        if len(current) >= k:
            __winning_possible["l_diag"] += current
            current = []            

    #check right diag
    for row in range(__rows):
        column = __columns - 1
        current = []
        while row >= 0 and column >= 0:
            if square == ' ' or square == __side:
                current.append((row, column))
            else:           
                if len(current) >= k:
                    __winning_possible["r_diag"] += current
                    current = []
            row -= 1
            column -= 1    
    if len(current) >= k:
        __winning_possible["r_diag"] += current
        current = []     

def zobrist_hash(board):
    global __zArray

    h = 0
    rows = len(board)
    cols = len(board[0])

    for row in range(rows):
        for col in range(cols):
            square = board[row][col]
            if square == 'X' or square == 'O':
                j = 0 if square == 'X' else 1
                h = h ^ __zArray[row][col][j]

    return h

    


INITIAL_STATE = \
              [[['X',' ','X'],
                [' ','O','O'],
                [' ',' ',' ']], "X"]

FIVE_ROW = \
              [[['-',' ',' ',' ',' ',' ','-'],
                [' ','X',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ','X',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                ['-',' ',' ',' ',' ',' ','-']], "X"]                

prepare(FIVE_ROW, 3, "5", "blah")                
# print(__zArray[0][0][0])
# print(__zArray[0][2][0])
#print(zobrist_hash(FIVE_ROW[0]))
