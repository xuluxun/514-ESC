# EightPuzzleWithHeuristics.py
# Luxun Xu
# CSE 415 HW 3 Part II 4

from math import sqrt

#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Basic Eight Puzzle"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Luxun Xu']
PROBLEM_CREATION_DATE = "20-APR-2016"
PROBLEM_DESC=\
'''This formulation of the Basic Eight Puzzle problem uses generic
Python 3 constructs and has been tested with Python 3.4.
It is designed to work according to the QUIET tools interface.
'''
#</METADATA>

#<COMMON_CODE>
def DEEP_EQUALS(s1,s2):
  result = True
  for i in range(9):
      if s1[i] != s2[i]:
          result = False
          break
  return result


def DESCRIBE_STATE(s):
  # Produces a textual description of a state.
  text = ""
  for i in range(9):
      text += str(s[i]) + "\t"
      if i % 3 == 2:
          text += "\n"
  return text


def HASHCODE(s):
  '''The result should be an immutable object such as a string
  that is unique for the state s.'''
  return str(s)

def copy_state(s):
  # Performs an appropriately deep copy of a state,
  # for use by operators in creating new states.
  news = []
  for new in s:
      news.append(new)
  return news

def can_move(s, direction):
  '''Tests whether it's legal to move the blank space to somewhere.'''
  try:
    zero_position = s.index(0)
    if zero_position in range(3) and direction == -3: return False
    if zero_position % 3 == 0 and direction == -1: return False
    if zero_position % 3 == 2 and direction == 1: return False
    if zero_position in range(6, 9) and direction == 3: return False
    return True
  except (Exception) as e:
    print(e)

def move(s, direction):
  '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the blank square
     to the direction position.'''
  news = copy_state(s) # start with a deep copy.
  zero_position = s.index(0)
  new_position = zero_position + direction
  exchange_number = s[new_position]
  news[new_position] = 0
  news[zero_position] = exchange_number
  return news # return new state

def goal_test(s):
  '''The goal state is from 0 to 8.'''
  return s == [0, 1, 2, 3, 4, 5, 6, 7, 8]

def goal_message(s):
  return "The Eight Puzzle is Solved!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

def CHECK_INI_STATE(s):
    inv_count = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if s[i] and s[j] and s[i] > s[j]:
                inv_count += 1
    #print(inv_count)
    return inv_count

#</COMMON_CODE>

def h_euclidean(s):
    distance = 0
    goal = GOAL_STATE
    for i in s:
        s_index = s.index(i)
        g_index = goal.index(i)
        x = s_index / 3
        y = s_index % 3
        g_x = g_index / 3
        g_y = g_index % 3
        distance += sqrt(pow(x - g_x, 2) + pow(y - g_y, 2))

    return distance

def h_hamming(s):
    distance = 0
    goal = GOAL_STATE
    for i in s:
        s_index = s.index(i)
        g_index = goal.index(i)
        if s_index != g_index:
            distance += 1

    return distance

def h_manhattan(s):
    distance = 0
    goal = GOAL_STATE
    for i in s:
        s_index = s.index(i)
        g_index = goal.index(i)
        x = s_index / 3
        y = s_index % 3
        g_x = g_index / 3
        g_y = g_index % 3
        distance += abs(x - g_x) + abs(y - g_y)
    return distance

def h_custom(s):
    distance = h_manhattan(s)
    inv_count = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if s[i] and s[j] and s[i] == s[j] + 1:
                inv_count += 2
    return distance + inv_count

#<COMMON_DATA>
N = 3
GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]
#</COMMON_DATA>

#<INITIAL_STATE>
#INITIAL_STATE = [1, 0, 2, 3, 4, 5, 6, 7, 8]
#CREATE_INITIAL_STATE = lambda: [3, 1, 2, 4, 0, 5, 6, 7, 8]
#DUMMY_STATE =  {'peg1':[], 'peg2':[], 'peg3':[] }
#</INITIAL_STATE>

#<OPERATORS>
directions = [-3, -1, 1, 3]
OPERATORS = [Operator("Move black space in direction of " + str(direction) + ".",
                      lambda s, direction=direction: can_move(s, direction),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, direction=direction: move(s, direction))
             for direction in directions]
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

HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming': h_hamming, 'h_manhattan': h_manhattan, 'h_custom': h_custom}