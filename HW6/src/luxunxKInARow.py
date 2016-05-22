'''Luxun Xu
   CSE 415 HW 5 Option B'''

import time
import math

N = 0
M = 0
FORBIDDEN = []
K = 0
SIDE = ''
OPPONENT = ''


def prepare(initial_state, k, what_side_I_play, opponent_nick_name):
    board = initial_state[0]
    global N, M, FORBIDDEN, OPPONENT, SIDE, K
    K = k
    SIDE = what_side_I_play
    OPPONENT = opponent_nick_name
    N = len(board)
    M = len(board[0])
    for i in range(N):
        for j in range(M):
            if board[i][j] == "-":
                FORBIDDEN.append((i, j))
    return "READY"


def introduce():
    intro = "Hi. This is Alpha_Xu. I am designed by Luxun XU (NetID: luxunx). I am aggressive and designed to win!"
    return intro


def nickname():
    return "Alpha_XU"


def makeMove(CurrentState, currentRemark, timeLimit=10000):
    timeWhenStart = time.time()
    values = minimax(CurrentState, timeLimit, timeWhenStart, 2)
    newState = values[1]
    score = values[0]
    n_row = 0
    n_col = 0
    newRemark = ""
    #print(str(score))
    if score == 0:
        newRemark = "It is still a fair game."
    elif score >= math.pow(10, K + 2):
        newRemark = "Accept your loss now. You can't beat me."
    elif score <= -math.pow(10, K + 2):
        newRemark = "You are too good. I cannot beat you."
    elif score < 0:
        newRemark = "You may have slight advantage but I will find a way back."
    else:
        newRemark = "I think I am winning right now."
    for i in range(N):
        for j in range(M):
            if CurrentState[0][i][j] != newState[0][i][j]:
                n_row = i
                n_col = j
                break
    move = (n_row, n_col)
    result = [[move, newState], newRemark]
    return result


def minimax(state, timeLimit, timeStart, playLeft):
    if time.time() - timeStart >= timeLimit * 0.9: return [staticEval(state), state]
    newState = []
    side = state[1]
    if playLeft == 0: return [staticEval(state), state]
    if side == SIDE: provisional = -math.pow(10, K + 3)
    else: provisional = math.pow(10, K + 3)
    for everyState in successors(state, side):
        everyResult = minimax(everyState, timeLimit, timeStart, playLeft - 1)
        newVal = everyResult[0]
        #print('here')
        if (side == SIDE and newVal > provisional) or (side == other(SIDE) and newVal < provisional):
            provisional = newVal
            newState = everyState
    #print(str(provisional))
    #print(newState)
    return [provisional, newState]


def successors(state, whoseMove):
    board = state[0]
    news = []
    for i in range(N):
        for j in range(M):
            if board[i][j] == ' ':
                temp = deep_copy(board)
                temp[i][j] = whoseMove
                new = [temp, other(whoseMove)]
                news.append(new)
    return news


def staticEval(state):
    score = eval_helper(state)
    return score


def other(SIDE):
    if SIDE == "X":
        return "O"
    elif SIDE == "O":
        return "X"


def eval_helper(state):
    board = state[0]
    score = 0
    max_positive = 0
    max_negative = 0
    for i in range(N):
        for j in range(M):
            if (i, j) not in FORBIDDEN:
                # Horizontal
                count_X = 0
                count_O = 0
                count = 0
                for l in range(K):
                    if (i, j + l) not in FORBIDDEN and j + l < M:
                        count += 1
                        if board[i][j + l] == 'X':
                            count_X += 1
                        elif board[i][j + l] == 'O':
                            count_O += 1
                if count == K:
                    if count_X == K:
                        max_positive = math.pow(10, K + 2)
                    elif count_O == K:
                        max_negative -math.pow(10, K + 2)
                    elif count_X == 0 and count_O == 0:
                        score = score
                    elif count_X == 0:
                        score -= math.pow(10, count_O)
                    elif count_O == 0:
                        score += math.pow(10, count_X)
                # Vertical
                count_X = 0
                count_O = 0
                count = 0
                for l in range(K):
                    if (i + l, j) not in FORBIDDEN and i + l < N:
                        count += 1
                        if board[i + l][j] == 'X':
                            count_X += 1
                        elif board[i + l][j] == 'O':
                            count_O += 1
                if count == K:
                    if count_X == K:
                        max_positive = math.pow(10, K + 2)
                    elif count_O == K:
                        max_negative = -math.pow(10, K + 2)
                    elif count_X == 0 and count_O == 0:
                        score = score
                    elif count_X == 0:
                        score -= math.pow(10, count_O)
                    elif count_O == 0:
                        score += math.pow(10, count_X)
                # Diagonal
                count_X = 0
                count_O = 0
                count = 0
                for l in range(K):
                    if (i + l, j + l) not in FORBIDDEN and j + l < M and i + l < N:
                        count += 1
                        if board[i + l][j + l] == 'X':
                            count_X += 1
                        elif board[i + l][j + l] == 'O':
                            count_O += 1
                if count == K:
                    if count_X == K:
                        max_positive = math.pow(10, K + 2)
                    elif count_O == K:
                        max_negative = -math.pow(10, K + 2)
                    elif count_X == 0 and count_O == 0:
                        score = score
                    elif count_X == 0:
                        score -= math.pow(10, count_O)
                    elif count_O == 0:
                        score += math.pow(10, count_X)
                count_X = 0
                count_O = 0
                count = 0
                for l in range(K):
                    if (i + l, j - l) not in FORBIDDEN and i + l < N and j - l >= 0:
                        count += 1
                        if board[i + l][j - l] == 'X':
                            count_X += 1
                        elif board[i + l][j - l] == 'O':
                            count_O += 1
                if count == K:
                    if count_X == K:
                        max_positive = math.pow(10, K + 2)
                    elif count_O == K:
                        max_negative = -math.pow(10, K + 2)
                    elif count_X == 0 and count_O == 0:
                        score = score
                    elif count_X == 0:
                        score -= math.pow(10, count_O)
                    elif count_O == 0:
                        score += math.pow(10, count_X)
    if max_positive != 0:
        return max_positive
    elif max_negative != 0:
        return max_negative
    else:
        return score


def deep_copy(board):
    news = []
    for i in range(N):
        new = []
        for j in range(M):
            new.append(board[i][j])
        news.append(new)
    return news
