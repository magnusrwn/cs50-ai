"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for row in board:
        for item in row:
            if item != EMPTY: count +=1
    
    return X if count % 2 == 0 else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i, row in enumerate(board):
        for j, item in enumerate(row):
            if board[i][j] == EMPTY: possible_actions.add((i, j))
    return possible_actions if len(possible_actions) != 0 else None

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_ = player(board)
    i = action[0]
    j = action[1]
    # if i not in vals or j not in vals:
        # print(i, j)
        # raise ValueError('i, or j were greater than 3, which is out of the boards indecies')
    b_copy = deepcopy(board)
    b_copy[i][j] = player_

    return b_copy
# logic err

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    bin = {is_row_win(board), is_column_win(board), is_right_win(board), is_left_win(board)}
    if X in bin: return X
    if O in bin: return O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return True if winner(board) or not actions(board) else False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_ = winner(board)
    if winner_ == "X": return 1
    elif winner_ == "O": return -1
    else: return 0

def minimax(board, depth, maximising_player, alpha, beta):
    """
    Returns the optimal action for the current player on the board.
    """
    # check if the board is terminal, or for winners
    if terminal(board) or depth == 0:
        score = utility(board)
        if maximising_player:
            return None, (score - depth)
        else:
            return None, (score + depth)

    best_move = None
    if maximising_player:
        max_eval = -math.inf
        for action in actions(board):
            _, eval = minimax(result(board, action), depth -1, False, alpha, beta)
            if max_eval < eval:
                best_move = action
                max_eval = eval
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return best_move
    else:
        min_eval = math.inf
        for action in actions(board):
            _, eval = minimax(result(board, action), depth -1, True, alpha, beta)
            if eval < min_eval:
                best_move = action
                min_eval = eval
            beta = min(alpha, eval)
            if beta <= alpha:
                break
        return best_move
        

def is_row_win(board):
    for row in board:
        if all(item == X for item in row):
            return X
        if all(item == O for item in row):
            return O
    return None

def is_right_win(board):
    # add the items to the set
    diagonal_list = [board[0][2], board[1][1], board[2][0]]
    if all(item == X for item in diagonal_list):
        return X
    if all(item == O for item in diagonal_list):
        return O
    return None

def is_left_win(board):
    # add the items to the set
    diagonal_list = [board[0][0], board[1][1], board[2][2]]
    if all(item == X for item in diagonal_list):
        return X
    if all(item == O for item in diagonal_list):
        return O
    return None

def is_column_win(board):
    for i in range(0, len(board)):
        col = [board[0][i], board[1][i], board[2][i]]
        if all(item == X for item in col):
            return X
        if all(item == O for item in col):
            return O
    return None