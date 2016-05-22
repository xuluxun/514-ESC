# EightPuzzleWithHeuristics.py
# Luxun Xu & Eden Ghirmai
# CSE 415 HW 4


#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Sudoku"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Luxun Xu']
PROBLEM_CREATION_DATE = "29-APR-2016"
PROBLEM_DESC=\
'''This formulation of the Basic Eight Puzzle problem uses generic
Python 3 constructs and has been tested with Python 3.4.
It is designed to work according to the QUIET tools interface.
'''
#</METADATA>

#<COMMON_CODE>
def DEEP_EQUALS(s1,s2):
  result = True
  for i in range(N):
      if s1[i] != s2[i]:
          result = False
          break
  return result


def DESCRIBE_STATE(s):
  # Produces a textual description of a state.
  text = ""
  for i in range(N):
      text += s[i] + " "
      if i % 9 == 8:
          text += "\n"
  return text


def HASHCODE(s):
  '''The result should be an immutable object such as a string
  that is unique for the state s.'''
  return str(s)

def copy_state(s):
  # Performs an appropriately deep copy of a state,
  # for use by operators in creating new states.
  news = {}
  for i in range(N):
      news[i] = s[i]
  return news

def can_move(s, number, square):
  '''Tests whether it's legal to move the blank space to somewhere.'''
  #print(number + " " + str(square))
  try:
    if s[square] == []:
        return False
    if len(s[square]) <= 1:
        return False
    if number not in s[square]:
        return False
    return True
  except (Exception) as e:
    print(e)

def move(s, number, square):
  '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the blank square
     to the direction position.'''
  #print(number + " " + str(square))
  news = copy_state(s) # start with a deep copy.
  news[square] = number
  d = eliminate(news)
  #print(DESCRIBE_STATE(d))
  return d # return new state

def goal_test(s):
  for i in range(N):
      if len(s[i]) > 1 or s[i] == '':
          return False
  return True

def goal_message(s):
  return "The Sudoku is Solved!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)


def parse_puzzle(s):
    d = {}
    for i in range(N):
        if s[i] == '.' or s[i] == '0':
            d[i] = '123456789'
        else:
            d[i] = s[i]
    #print(DESCRIBE_STATE(d))
    return eliminate(d)


def eliminate(s):
    d = copy_state(s)
    still = True
    while still:
        still = False
        for i in range(N):
            if len(d[i]) > 1:
                for j in range(N):
                    if j != i and len(d[j]) == 1:
                        if i//9 == j//9 and d[j] in d[i]:
                            still = True
                            d[i] = d[i].replace(d[j], '')
                        elif (i-j) % 9 == 0 and d[j] in d[i]:
                            still = True
                            d[i] = d[i].replace(d[j], '')
                        elif i//27 == j//27 and i%9//3 == j%9//3 and d[j] in d[i]:
                            still = True
                            d[i] = d[i].replace(d[j], '')
    return d

def grid():
    list = []
    for i in range(N):
        list.append(i)
    return list

def h_custom1(s):
    distance = 0
    for i in range(N):
        if len(s[i]) > 1:
            distance += 1
    return distance

def h_custom2(s):
    distance = 0
    for i in range(N):
        distance += len(s[i])
    return distance


#</COMMON_CODE>

#<COMMON_DATA>
N = 81
PUZZLE_HARD =       '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
PUZZLE_MEDIUM1 =    '..4....575..1.8.3.....6....37.6...9..8.973.4..9...1.23....1.....2.7.5..195....3..'
PUZZLE_MEDIUM2 =    '008200006004005070007000850120708000090006000000104029052000100080500900700006200'
PUZZLE_MEDIUM3 =    '001086000000002508398000000003021000072000390000930600000000437405800000000260100'
PUZZLE_EASY =   '902040010013005904047130060004060090000408000070090400020057630708600540050010702'
#</COMMON_DATA>

#<INITIAL_STATE>
INITIAL_STATE = parse_puzzle(PUZZLE_MEDIUM3)
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
#DUMMY_STATE =  {'peg1':[], 'peg2':[], 'peg3':[] }
#</INITIAL_STATE>

#<OPERATORS>
numbers = ['1','2','3','4','5','6','7','8','9']
squares = grid()
combinations = [(square, number) for square in squares for number in numbers]

OPERATORS = [Operator("Move black space in direction of ",
                      lambda s, number=number, square=square: can_move(s, number, square),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, number=number, square=square: move(s, number, square))
             for (square, number) in combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
if 'BRYTHON' in globals():
 from TowersOfHanoiVisForBrython import set_up_gui as set_up_user_interface
 from TowersOfHanoiVisForBrython import render_state_svg_graphics as render_state
# if 'TKINTER' in globals(): from TicTacToeVisForTKINTER import set_up_gui
#</STATE_VIS>

HEURISTICS = {'h_custom1': h_custom1, 'h_custom2': h_custom2}