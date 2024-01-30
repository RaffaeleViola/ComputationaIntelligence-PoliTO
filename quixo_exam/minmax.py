import numpy as np
from game import Game, Move
from quixo_exam.utils import next_acts, is_accetptable


# max_cache = dict()
# min_cache = dict()


def rotate_board(board: np.ndarray):
    # 90 degree
    # it's clockwise
    r270 = np.rot90(board)
    r180 = np.rot90(r270)
    r90 = np.rot90(r180)
    return r90, r180, r270


def transform_move(cache_item: tuple[tuple[tuple[int, int], Move], float], degree: int) -> tuple[
    tuple[tuple[int, int], Move], float]:
    move, scr = cache_item
    pos = move[0]
    mv = move[1]
    # map_move = {Move.TOP: Move.RIGHT, Move.RIGHT: Move.BOTTOM, Move.BOTTOM: Move.LEFT, Move.LEFT: Move.TOP}
    map_move = {Move.TOP: Move.LEFT, Move.RIGHT: Move.TOP, Move.BOTTOM: Move.RIGHT, Move.LEFT: Move.BOTTOM}
    map_y_into_x = {0: 4, 4: 0, 1: 3, 3: 1, 2: 2}
    p270 = map_y_into_x[pos[1]], pos[0]
    p180 = map_y_into_x[p270[1]], p270[0]
    p90 = map_y_into_x[p180[1]], p180[0]
    if degree == 90:
        return (p90, map_move[mv]), scr
    elif degree == 180:
        return (p180, map_move[map_move[mv]]), scr
    else:
        return (p270, map_move[map_move[map_move[mv]]]), scr


def scoring_fun(game: Game, player: int, to_maximize: int):
    brd = game.get_board()

    max_rows = max([(brd[i, :] == player).sum() for i in range(5)])
    max_columns = max([(brd[:, i] == player).sum() for i in range(5)])
    diag1 = sum([(brd[i, i] == player).sum() for i in range(5)])
    diag2 = sum([(brd[i, j] == player).sum() for i, j in zip(range(5), range(4, -1, -1))])
    mapping = {0: 0, 1: 1, 2: 10, 3: 100, 4: 1000, 5: 10_000}
    if player == to_maximize:
        return mapping[max_rows] + mapping[max_columns] + mapping[diag1] + mapping[diag2]
    else:
        return -(mapping[max_rows] + mapping[max_columns] + mapping[diag1] + mapping[diag2])


def minmax(game: Game, plyr_id, depth, alpha, beta, plyr_to_maximize: int, max_cache, min_cache) -> tuple[tuple[tuple[int, int], Move], float]:
    plyr_id += 1
    plyr_id %= 2
    cache = max_cache if plyr_id == plyr_to_maximize else min_cache
    # checking board and rotations in cache
    b90, b180, b270 = rotate_board(game.get_board())
    if (tuple(game.get_board().ravel()), depth) in cache:
        return cache[tuple(game.get_board().ravel()), depth]
    if (tuple(b90.ravel()), depth) in cache:
        return transform_move(cache[tuple(b90.ravel()), depth], 90)
    if (tuple(b180.ravel()), depth) in cache:
        return transform_move(cache[tuple(b180.ravel()), depth], 180)
    if (tuple(b270.ravel()), depth) in cache:
        return transform_move(cache[tuple(b270.ravel()), depth], 270)
    over = game.check_winner()
    next_actions = next_acts(game, plyr_id)
    if over != -1 or not next_actions or depth == 0:
        prev_plr = plyr_id + 1
        prev_plr %= 2
        res = scoring_fun(game, prev_plr, plyr_to_maximize)
        return None, res
    new_g = Game()
    new_g._board = game.get_board()
    new_g.current_player_idx = plyr_id
    best_move = None
    curr_alpha = alpha
    curr_beta = beta
    to_stop = False
    for move in next_actions:
        for direct in [Move.TOP, Move.LEFT, Move.RIGHT, Move.BOTTOM]:
            if not is_accetptable(move, direct, new_g):
                continue
            new_g = Game()
            new_g._board = game.get_board()
            new_g.current_player_idx = plyr_id
            new_g._Game__move(move, direct, plyr_id)
            _, score = minmax(new_g, plyr_id, depth - 1, curr_alpha, curr_beta, plyr_to_maximize, max_cache, min_cache)
            if plyr_id == plyr_to_maximize:  # to maximize
                if score > curr_alpha:
                    curr_alpha = score
                    best_move = (move, direct)
                if curr_alpha >= curr_beta:
                    to_stop = True
                    break
            else:
                if score < curr_beta:  # to_minimize
                    curr_beta = score
                    best_move = (move, direct)
                if curr_alpha >= curr_beta:
                    to_stop = True
                    break
            if best_move is None:
                best_move = (move, direct)
        if to_stop:
            break
    score_val = curr_alpha if plyr_id == plyr_to_maximize else curr_beta
    if best_move:
        cache[tuple(game.get_board().ravel()), depth] = best_move, score_val
    return best_move, score_val
