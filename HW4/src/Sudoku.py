''' Sudoku.py
Luxun Xu & Eden Ghirmai 
CSE415 Spr16 - 4/29/2015
Assignment 4: Problem Formulation
'''

#<METADATA>
PROBLEM_NAME = "Sudoku"
PROBLEM_AUTHORS = ['Eden Ghirmai', 'Luxun Xu']
PROBLEM_CREATION_DATE = "29-APR-2016"
PROBLEM_DESC=\
'''This formulation of the basic eight puzzle uses generic
Python 3 constructs and has been tested with Python 3.4.
It is designed to work according to the QUIET tools interface.
'''

#<COMMON_CODE>
def DEEP_EQUALS(s1, s2):
    if len(s1) != len(s2) or len(s1[0]) != len(s2[0]):
        return False
    for i in range(len(s1)):
        for j in range(len(s1)):
            if s1[i][j] != s2[i][j]:
                return False
    return True

def DESCRIBE_STATE(s):
    return render_state(s)

def HASHCODE(s):
    return str(s)

def copy_state(s):
    new = [[-1 for x in range(9)] for y in range(9)]
    for i in range(len(s)):
        for j in range(len(s)):
            new[i][j] = s[i][j]
    return new

def goal_test(s):
    for i in range(len(s)):
        for j in range(len(s)):
            if s[i][j] == -1:
                return False
                return True

def goal_message(s):
    return "Your Sudoku has been solved!!"


class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

def move(s, n, x, y):
    new = copy_state(s)
    new[x][y] = n
    return new


def can_move(s, n, x, y):
    if (s[x][y] != -1):
        return False

    #check row
    row = s[x]
    for num in row:
        if num == n:
            return False

    #check col
    for row in s:
        if row[y] == n:
            return False

    #check box
    for row in range(3):
        for col in range(3):
            if s[row + (x - x % 3)][col + (y - y % 3)] == n:
                return False
    return True

#</COMMON_CODE>

def h_custom(s):
    result = 0
    print(str(len(s)))
    for i in range(len(s)):
        for j in range(len(s)):
            if s[i][j] != -1:
                result += 1
    return result

#<COMMON_DATA>
GRID_SIZE = 81
#</COMMON_DATA>

#<INITIAL_STATE>
# -1 resembles an empty spot

# http://www.theguardian.com/lifeandstyle/2016/apr/28/sudoku-3421-hard
INITIAL_STATE =  [[-1, 1, -1, -1, 3, -1, -1, 8, -1],
                  [8, -1, 6, -1, -1, -1, 3, -1, 9],
                  [-1, -1, 4, 9, -1, -1, -1, 7, -1],
				  [-1, -1, 9, -1, 4, 7, -1, -1, -1],
				  [-1, -1, -1, -1, -1, 1, -1, -1, 5],
				  [-1, -1, 1, -1, -1, -1, 6, -1, -1],
				  [-1, 7, -1, 6, -1, 8, 4, 9, -1],
				  [-1, 8, 3, -1, -1, -1, -1, -1, 2],
				  [6, -1, -1, -1, -1, -1, -1, 5, -1]]


# http://www.sudokukingdom.com/very-easy-sudoku.php
EASY_GAME = [[-1, 7, 2, -1,  -1, 1, 8,  -1, 5],
			 [-1, 5, 1, -1, 3, 7, -1, 9, -1],
			 [4, -1, -1, 2, -1, 8, 1, -1, 7],
			 [-1, 4, 7, 5, 2, -1, 3, -1, -1],
			 [-1, 2, 6, 7, -1, -1, 5, -1, 1],
			 [5, -1, -1, 1, -1, 6, -1, 2, 9],
			 [2, 9, -1, 3, 7, -1, -1, 1, -1],
			 [7, -1, -1, -1, 6, 2, -1, 5, 3],
			 [3, -1, 8, -1, 1, -1, 2, 7, -1]]



CREATE_INITIAL_STATE = lambda: EASY_GAME

#</INITIAL_STATE>

#<OPERATORS>
options = [1,2,3,4,5,6,7,8,9]
blanks = []
temp = copy_state(CREATE_INITIAL_STATE())
for x in range(9):
    for y in range(9):
        can_moves = []
        for n in range(1, 10):
            if can_move(temp, n, x, y):
                can_moves.append((n, x, y))

        if len(can_moves) == 1:
            temp = move(temp, can_moves[0][0], can_moves[0][1], can_moves[0][2])
        else:
            for option in can_moves:
                options.append(option)



OPERATORS = [Operator("Add number " + str(n) + " to row " + str(x) + " and column " + str(y),
                      lambda s, n=n, x=x,  y=y: can_move(s, n, x, y),
                      lambda s, n=n, x=x, y=y: move(s, n, x, y))
             for (n, x, y) in options]

#</OPERATORS>

#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> 
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
'''
 .  1  . | .  3  . | .  8  . 
 8  .  6 | .  .  . | 3  .  9 
 .  .  4 | 9  .  . | .  7  . 
----------------------------
 .  .  9 | .  4  7 | .  .  . 
 .  .  . | .  .  1 | .  .  5 
 .  .  1 | .  .  . | 6  .  . 
----------------------------
 .  7  . | 6  .  8 | 4  9  . 
 .  8  3 | .  .  . | .  .  2 
 6  .  . | .  .  . | .  6  . 

'''

def render_state(s):
	text = "\n"
	for i in range(len(s)):
		for j in range(len(s[0])):
			if s[i][j] == -1:
				text += " . "
			else:
				text += " " + str(s[i][j]) + " "

			if j == 2 or j == 5: # TO-DO: Avoid hard coding if time
				text += "|"

		text += "\n"
		if i == 2 or i == 5: # TO-DO: Avoid hard coding if time
			text += "----------------------------\n"

	return text
 
#</STATE_VIS>


HEURISTICS = {'h_custom':h_custom}
