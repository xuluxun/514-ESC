'''MDP.py
S. Tanimoto, May 2016.

Provides representations for Markov Decision Processes, plus
functionality for running the transitions.

The transition function should be a function of three arguments:
T(s, a, sp), where s and sp are states and a is an action.
The reward function should also be a function of the three same
arguments.  However, its return value is not a probability but
a numeric reward value -- any real number.

operators:  state-space search objects consisting of a precondition
 and deterministic state-transformation function.
 We assume these are in the "QUIET" format used in earlier assignments.

actions:  objects (for us just Python strings) that are 
 stochastically mapped into operators at runtime according 
 to the Transition function.


Status:
 As of May 14 at 11:00 AM:
   Basic methods have been prototyped.


'''

'''Edited by Luxun XU 1334990
as HW 6 Part II for CSE 415
'''

import random

REPORTING = True

class MDP:
    def __init__(self):
        self.known_states = set()
        self.succ = {} # hash of adjacency lists by state.

    def register_start_state(self, start_state):
        self.start_state = start_state
        self.known_states.add(start_state)

    def register_actions(self, action_list):
        self.actions = action_list

    def register_operators(self, op_list):
        self.ops = op_list

    def register_transition_function(self, transition_function):
        self.T = transition_function

    def register_reward_function(self, reward_function):
        self.R = reward_function

    def state_neighbors(self, state):
        '''Return a list of the successors of state.  First check
           in the hash self.succ for these.  If there is no list for
           this state, then construct and save it.
           And then return the neighbors.'''
        neighbors = self.succ.get(state, False)
        if neighbors==False:
            neighbors = [op.apply(state) for op in self.ops if op.is_applicable(state)]
            self.succ[state]=neighbors
            self.known_states.update(neighbors)
        return neighbors

    def random_episode(self, nsteps):
        self.current_state = self.start_state
        self.current_reward = 0.0
        for i in range(nsteps):
            self.take_action(random.choice(self.actions))
            if self.current_state == 'DEAD':
                print('Terminating at DEAD state.')
                break
        if REPORTING: print("Done with "+str(i)+" of random exploration.")

    def take_action(self, a):
        s = self.current_state
        neighbors = self.state_neighbors(s)
        threshold = 0.0
        rnd = random.uniform(0.0, 1.0)
        r = 0
        for sp in neighbors:
            threshold += self.T(s, a, sp)
            if threshold>rnd:
                r = self.R(s, a, sp)
                break
        self.current_state = sp
        if REPORTING: print("After action "+a+", moving to state "+str(sp)+\
                            "; reward is "+str(r))

    def generateAllStates(self):
        OPEN = [self.start_state]
        CLOSED = []

        while OPEN != []:
            S = OPEN[0]
            del OPEN[0]
            CLOSED.append(S)

            L = []
            for op in self.ops:
                if op.precond(S):
                    new_state = op.state_transf(S)
                    if new_state not in CLOSED:
                        L.append(new_state)

            for s2 in L:
                for i in range(len(OPEN)):
                    if s2 == OPEN[i]:
                        del OPEN[i]
                        break

            OPEN = L + OPEN
        CLOSED.remove((0,0))
        for s in CLOSED:
            self.known_states.add(s)

    def valueIterations(self, discount, niterations):
        self.V = {}
        self.VStar = {}
        for s in self.known_states:
            self.V[s] = 0
            self.VStar[s] = 0
        for i in range(niterations):
            #print(str(i) + " Iteration:")
            #print(self.V)
            #print(self.VStar)
            for s in self.known_states:
                maxValue = -99999999999999.9
                for a in self.actions:
                    newValue = 0.0
                    for sp in self.state_neighbors(s):
                        newValue += self.T(s, a, sp) * (self.R(s, a, sp) + discount*self.V[sp])
                    maxValue = max(maxValue, newValue)
                self.VStar[s] = maxValue
            for s in self.known_states:
                temp = self.VStar[s]
                self.V[s] = temp

    def QLearning(self, discount, nEpisodes, epsilon):
        self.QValues = {}
        self.QValuesStar = {}
        NAction = {}
        for s in self.known_states:
            for a in self.actions:
                self.QValues[(s, a)] = 0
                self.QValuesStar[(s, a)] = 0
                NAction[(s, a)] = 1
        action = ['North', 'South', 'East', 'West']
        for i in range(nEpisodes):
            #count = 0
            self.current_state = self.start_state
            while self.current_state != 'DEAD':
                #count += 1
                rnd = random.uniform(0.0, 1.0)
                s = self.current_state
                if rnd < epsilon and s != (3, 1) and s != (3, 2):
                    #act randomly
                    a = random.choice(action)
                    NAction[(s, a)] += 1
                    alpha = 1 / NAction[(s, a)]
                    sp = self.move(s, a)
                    maxValue = max(self.QValues[(sp, i)] for i in self.actions)
                    if sp == (3, 1) or sp == (3, 2):
                        maxValue = self.QValues[(sp, 'End')]
                    sample = self.R(s, a, sp) + discount * maxValue
                    self.QValuesStar[(s, a)] = (1 - alpha) * self.QValues[(s, a)] + alpha * sample
                else:
                    if s == (3, 1) or s == (3, 2):
                        a = 'End'
                    else:
                        maxP = -999999999.9
                        a = ''
                        for i in action:
                            if self.QValues[(s, i)] > maxP:
                                maxP = self.QValues[(s, i)]
                                a = i
                    NAction[(s, a)] += 1
                    alpha = 1 / NAction[(s, a)]
                    sp = self.move(s, a)
                    maxValue = max(self.QValues[(sp, i)] for i in self.actions)
                    if sp == (3, 1) or sp == (3, 2):
                        maxValue = self.QValues[(sp, 'End')]
                    sample = self.R(s, a, sp) + discount * maxValue
                    self.QValuesStar[(s, a)] = (1 - alpha) * self.QValues[(s, a)] + alpha * sample
                self.current_state = sp
            for s in self.QValuesStar:
                temp = self.QValuesStar[s]
                self.QValues[s] = temp
            #print(str(count))
            #print(str(i) + " episode:")
            #print(self.QValues)
            #print(self.QValuesStar)

    def move(self, state, action):
        x, y = state
        if action == 'North':
            if (x, y + 1) in self.known_states:
                newState = (x, y + 1)
                return newState
            else:
                return state
        elif action == 'South':
            if (x, y - 1) in self.known_states:
                newState = (x, y - 1)
                return newState
            else:
                return state
        elif action == 'East':
            if (x + 1, y) in self.known_states:
                newState = (x + 1, y)
                return newState
            else:
                return state
        elif action == 'West':
            if (x - 1, y) in self.known_states:
                newState = (x - 1, y)
                return newState
            else:
                return state
        elif action == 'End':
            return "DEAD"

    def extractPolicy(self, QValues):
        self.optPolicy = {}
        maxValues = {}
        for key in QValues:
            s = key[0]
            if s != 'DEAD':
                a = key[1]
                if s == (3, 1) or s == (3, 2):
                    if a == 'End':
                        self.optPolicy[s] = a
                else:
                    if a != 'End':
                        if s not in maxValues:
                            maxValues[s] = QValues[key]
                            self.optPolicy[s] = a
                        else:
                            if QValues[key] > maxValues[s]:
                                maxValues[s] = QValues[key]
                                self.optPolicy[s] = a
        #print(self.optPolicy)