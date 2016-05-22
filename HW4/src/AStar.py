''' AStar.py
Eden Ghirmai
CSE415 Spr16 - 4/20/2015
Assignment 3: Counting States and Working with A* Search
Examples of Usage:
python3 AStar.py EightPuzzleWithHeuristics h_custom
'''

import sys
import queue

if sys.argv==[''] or len(sys.argv)<4:
  import SudokuWithHeuristics as Problem
  h_heuristics = Problem.HEURISTICS['h_custom2']
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])
  h_heuristics = Problem.HEURISTICS[sys.argv[2]]
  Puzzle = importlib.import_module(sys.argv[3])

print("\nWelcome to A*")
COUNT = None
BACKLINKS = {}

def runAstar():
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(Problem.DESCRIBE_STATE(initial_state))
  global COUNT, BACKLINKS
  COUNT = 0
  BACKLINKS = {}
  Astar(initial_state)
  print(str(COUNT)+" states examined.")

def Astar(initial_state):
  global COUNT, BACKLINKS

  OPEN = [initial_state]
  CLOSED = []
  BACKLINKS[Problem.HASHCODE(initial_state)] = -1

  h_count = h_heuristics(initial_state)
  g_score = {Problem.HASHCODE(initial_state): 0}
  h_score = {Problem.HASHCODE(initial_state): h_count}
  f_score = {Problem.HASHCODE(initial_state): h_count}

  q = queue.PriorityQueue()
  q.put(initial_state)

  while OPEN != []:
    S = OPEN[0]
    prev_score = f_score[Problem.HASHCODE(S)]
    for element in OPEN:
      if f_score[Problem.HASHCODE(element)] < prev_score:
        S = element
        prev_score = f_score[Problem.HASHCODE(element)]

    del OPEN[OPEN.index(S)]
    CLOSED.append(S)

    if Problem.GOAL_TEST(S):
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      backtrace(S)
      return

    COUNT += 1
    if (COUNT % 32)==0:
       print(".",end="")
       if (COUNT % 128)==0:
         print("COUNT = "+str(COUNT))
         print("len(OPEN)="+str(len(OPEN)))
         print("len(CLOSED)="+str(len(CLOSED)))

    L = []
    for op in Problem.OPERATORS:
      #Optionally uncomment the following when debugging
      #a new problem formulation.
      #print("Trying operator: "+op.name)
      if op.precond(S):
        new_state = op.state_transf(S)
        if not occurs_in(new_state, CLOSED):
          brand_new_state = new_state not in OPEN
          lesser_score = False

          if brand_new_state:
            OPEN.append(new_state)
          else:
            lesser_score = g_score[Problem.HASHCODE(S)] <= g_score[Problem.HASHCODE(new_state)]

          if brand_new_state or lesser_score:
            BACKLINKS[Problem.HASHCODE(new_state)] = S
            new_state_hash = Problem.HASHCODE(new_state)
            g_score[new_state_hash] = g_score[Problem.HASHCODE(S)] + 1
            h_score[new_state_hash] = h_heuristics(new_state)
            f_score[new_state_hash] = g_score[Problem.HASHCODE(new_state)] + h_score[Problem.HASHCODE(new_state)]

    for s2 in L:
      for i in range(len(OPEN)):
        if Problem.DEEP_EQUALS(s2, OPEN[i]):
          del OPEN[i]; break

def backtrace(S):
  global BACKLINKS

  path = []
  while not S == -1:
    path.append(S)
    S = BACKLINKS[Problem.HASHCODE(S)]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(Problem.DESCRIBE_STATE(s))
  return path


def occurs_in(s1, lst):
  for s2 in lst:
    if Problem.DEEP_EQUALS(s1, s2): return True
  return False


if __name__=='__main__':
  runAstar()