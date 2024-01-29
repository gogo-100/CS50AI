"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def count_empty(board):
    empty_count = 0
    for line in board:
        for item in line:
            if item is EMPTY:
                empty_count += 1
    return empty_count


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    return X if count_empty(board) % 2 == 1 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                action.add((i,j))
    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        print(action)
        print(actions(board))
        raise RuntimeError("action is wrong")
    
    result_board = copy.deepcopy(board)
    result_board[action[0]][action[1]] = player(board)
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    temp_board = copy.deepcopy(board)
    for i in range(3):
        for j in range(3):
            if temp_board[i][j] is EMPTY:
                temp_board[i][j] = "E"
    res = set()
    #  horizontally,
    res.add(temp_board[0][0] + temp_board[0][1] + temp_board[0][2])
    res.add(temp_board[1][0] + temp_board[1][1] + temp_board[1][2])
    res.add(temp_board[2][0] + temp_board[2][1] + temp_board[2][2])
    #  vertically,
    res.add(temp_board[0][0] + temp_board[1][0] + temp_board[2][0])
    res.add(temp_board[0][1] + temp_board[1][1] + temp_board[2][1])
    res.add(temp_board[0][2] + temp_board[1][2] + temp_board[2][2])
    #  diagonally.
    res.add(temp_board[0][0] + temp_board[1][1] + temp_board[2][2])
    res.add(temp_board[2][0] + temp_board[1][1] + temp_board[0][2])
    
    if "XXX" in res:
        return X
    elif "OOO" in res:
        return O
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return count_empty(board) == 0 or winner(board) is not None 


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win is None:
        return 0
    elif win == X:
        return 1
    else:
        return -1


def mostValue(state,index):
    """
    The value of this node is not determined by its utility, 
    but is recursively determined by the values of the lower level nodes of this node
    """
    vals = [9999, -9999]
    funcs = [min, max]
    targets = [-1, 1]

    val = vals[index]
    if terminal(state):
        return utility(state)
    for action in actions(state):
        val = funcs[index](val, mostValue(result(state,action), 1-index))
        if val == targets[index]: # pruning
            return val
    return val

def minimax(board):
    if terminal(board):
        return None
    
    most_value = None
    most_action = None
    index = 0 if player(board) == X else 1
    funcs = [min, max]
    targets = [1, -1]

    for action in actions(board):
        val = mostValue(result(board,action), index)
        if most_value is None or funcs[index](most_value, val) == most_value:
            most_value = val
            most_action = action
        if val == targets[index]: # pruning
            return most_action
    return most_action
    