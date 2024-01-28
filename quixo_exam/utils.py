from game import Game, Move


def next_acts(game: Game, player: int):
    res = []
    board = game.get_board()
    for i in range(5):
        if board[0, i] == player or board[0, i] == -1:
            res.append((i, 0))
        if board[4, i] == player or board[4, i] == -1:
            res.append((i, 4))
    for i in range(1, 4):
        if board[i, 0] == player or board[i, 0] == -1:
            res.append((0, i))
        if board[i, 4] == player or board[i, 4] == -1:
            res.append((4, i))
    return res


def is_accetptable(pos, slide, game: Game):  # it takes standard coordinates x,y (row, col)
    # swapping for coordinates compliance
    from_pos = (pos[1], pos[0])
    acceptable: bool = (
                           # check if it is in the first row
                               (from_pos[0] == 0 and from_pos[1] < 5)
                               # check if it is in the last row
                               or (from_pos[0] == 4 and from_pos[1] < 5)
                               # check if it is in the first column
                               or (from_pos[1] == 0 and from_pos[0] < 5)
                               # check if it is in the last column
                               or (from_pos[1] == 4 and from_pos[0] < 5)
                           # and check if the piece can be moved by the current player
                       ) and (game.get_board()[from_pos] < 0 or game.get_board()[from_pos] == game.current_player_idx)
    if not acceptable:
        return False
    SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
    # if the piece position is not in a corner
    if from_pos not in SIDES:
        # if it is at the TOP, it can be moved down, left or right
        acceptable_top: bool = from_pos[0] == 0 and (
                slide == Move.BOTTOM or slide == Move.LEFT or slide == Move.RIGHT
        )
        # if it is at the BOTTOM, it can be moved up, left or right
        acceptable_bottom: bool = from_pos[0] == 4 and (
                slide == Move.TOP or slide == Move.LEFT or slide == Move.RIGHT
        )
        # if it is on the LEFT, it can be moved up, down or right
        acceptable_left: bool = from_pos[1] == 0 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.RIGHT
        )
        # if it is on the RIGHT, it can be moved up, down or left
        acceptable_right: bool = from_pos[1] == 4 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.LEFT
        )
    # if the piece position is in a corner
    else:
        # if it is in the upper left corner, it can be moved to the right and down
        acceptable_top: bool = from_pos == (0, 0) and (
                slide == Move.BOTTOM or slide == Move.RIGHT)
        # if it is in the lower left corner, it can be moved to the right and up
        acceptable_left: bool = from_pos == (4, 0) and (
                slide == Move.TOP or slide == Move.RIGHT)
        # if it is in the upper right corner, it can be moved to the left and down
        acceptable_right: bool = from_pos == (0, 4) and (
                slide == Move.BOTTOM or slide == Move.LEFT)
        # if it is in the lower right corner, it can be moved to the left and up
        acceptable_bottom: bool = from_pos == (4, 4) and (
                slide == Move.TOP or slide == Move.LEFT)
    # check if the move is acceptable
    acceptable: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right
    return acceptable
