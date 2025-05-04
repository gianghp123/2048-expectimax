import numpy as np
from puzzle import test_move
import math
from functools import lru_cache

#Heuristic scoring constants
# SCORE_LOST_PENALTY = 200000.0
# SCORE_MONOTONICITY_POWER = 4.0
# SCORE_MONOTONICITY_WEIGHT = 47.0
# SCORE_SUM_POWER = 3.5
# SCORE_SUM_WEIGHT = 11.0
# SCORE_MERGES_WEIGHT = 700.0
# SCORE_EMPTY_WEIGHT = 270.0

# def score_row(row):
#     """
#     Compute heuristic score for a single row or column.
#     """
#     sum_tiles = 0.0
#     empty = 0
#     merges = 0
#     monotonicity_left = 0.0
#     monotonicity_right = 0.0
#     prev = None
#     counter = 0
#     # Convert tile values to ranks: 0 if empty, else log2(tile)
#     ranks = [0 if tile == 0 else int(math.log2(tile)) for tile in row]
#     for rank in ranks:
#         if rank == 0:
#             empty += 1
#         else:
#             sum_tiles += rank ** SCORE_SUM_POWER
#             if prev == rank:
#                 counter += 1
#             else:
#                 if counter > 0:
#                     merges += 1 + counter
#                 counter = 0
#             prev = rank
#     if counter > 0:
#         merges += 1 + counter
#     for i in range(1, 4):
#         if ranks[i-1] > ranks[i]:
#             monotonicity_left += ranks[i-1] ** SCORE_MONOTONICITY_POWER - ranks[i] ** SCORE_MONOTONICITY_POWER
#         else:
#             monotonicity_right += ranks[i] ** SCORE_MONOTONICITY_POWER - ranks[i-1] ** SCORE_MONOTONICITY_POWER
#     score = (SCORE_LOST_PENALTY +
#              SCORE_EMPTY_WEIGHT * empty +
#              SCORE_MERGES_WEIGHT * merges -
#              SCORE_MONOTONICITY_WEIGHT * min(monotonicity_left, monotonicity_right) -
#              SCORE_SUM_WEIGHT * sum_tiles)
#     return score

# def score_row(row):
#     """
#     Compute heuristic score for a single row or column, ignoring merges.
#     """
#     sum_tiles = 0.0
#     empty = 0
#     monotonicity_left = 0.0
#     monotonicity_right = 0.0
#     # Convert tile values to ranks: 0 if empty, else log2(tile)
#     ranks = [0 if tile == 0 else int(math.log2(tile)) for tile in row]
#     for rank in ranks:
#         if rank == 0:
#             empty += 1
#         else:
#             sum_tiles += rank ** SCORE_SUM_POWER
#     for i in range(1, 4):
#         if ranks[i-1] > ranks[i]:
#             monotonicity_left += ranks[i-1] ** SCORE_MONOTONICITY_POWER - ranks[i] ** SCORE_MONOTONICITY_POWER
#         else:
#             monotonicity_right += ranks[i] ** SCORE_MONOTONICITY_POWER - ranks[i-1] ** SCORE_MONOTONICITY_POWER
#     score = (SCORE_LOST_PENALTY +
#              SCORE_EMPTY_WEIGHT * empty -
#              SCORE_MONOTONICITY_WEIGHT * min(monotonicity_left, monotonicity_right) -
#              SCORE_SUM_WEIGHT * sum_tiles)
#     return score


SCORE_LOST_PENALTY = 200000.0
SCORE_MONOTONICITY_POWER = 4.0
SCORE_MONOTONICITY_WEIGHT =10
SCORE_EMPTY_WEIGHT = 10



# def score_row(row):
#     """
#     Compute heuristic score for a single row or column, prioritizing empty cells over monotonicity.
#     """
#     empty = 0
#     monotonicity_left = 0.0
#     monotonicity_right = 0.0
#     # Convert tile values to ranks: 0 if empty, else log2(tile)
#     ranks = [0 if tile == 0 else int(math.log2(tile)) for tile in row]
#     for rank in ranks:
#         if rank == 0:
#             empty += 1
#     for i in range(1, 4):
#         if ranks[i-1] > ranks[i]:
#             monotonicity_left += ranks[i-1] ** SCORE_MONOTONICITY_POWER - ranks[i] ** SCORE_MONOTONICITY_POWER
#         else:
#             monotonicity_right += ranks[i] ** SCORE_MONOTONICITY_POWER - ranks[i-1] ** SCORE_MONOTONICITY_POWER
#     score = (SCORE_LOST_PENALTY +
#              SCORE_EMPTY_WEIGHT * empty -
#              SCORE_MONOTONICITY_WEIGHT * min(monotonicity_left, monotonicity_right))
#     return score

# def cached_score_heur(board_tuple):
#     """
#     Compute the heuristic score for the entire 2048 board.
    
#     Args:
#         board_tuple: A tuple of 4 tuples, each containing 4 integers representing the tile values
#                      (e.g., 0, 2, 4, 8, ...).
    
#     Returns:
#         float: The heuristic score for the board.
#     """
#     # Calculate score for rows
#     row_scores = sum(score_row(row) for row in board_tuple)
#     # Transpose to get columns
#     transposed = tuple(zip(*board_tuple))
#     # Calculate score for columns
#     col_scores = sum(score_row(col) for col in transposed)
#     # Total heuristic score
#     total_score = row_scores + col_scores
#     return total_score

# import numpy as np
# from functools import lru_cache

class ExpectimaxOptimizer:
    def __init__(self, heuristic_func, max_workers=4):
        """Initialize optimizer with a heuristic function."""
        self.heuristic_func = heuristic_func
        self.max_workers = max_workers

    def score_heur_board(self, board):
        """Score the board using the provided heuristic function."""
        return self.heuristic_func(board)
    
    def execute_move(self, board, move):
        return test_move(board, move)
    
    def score_tilechoose_node(self, board_tuple, cprob, depth, max_depth):
        # Nếu xác suất tích lũy quá nhỏ hoặc độ sâu đạt giới hạn, trả về điểm heuristic
        if cprob < 0.0001 or depth >= max_depth:
            return self.score_heur_board(np.array(board_tuple, dtype=np.int64))
        
        board = np.array(board_tuple, dtype=np.int64)
        empty_positions = np.argwhere(board == 0)
        if empty_positions.size == 0:
            return 0.0
        
        num_open = len(empty_positions)
        prob_factor = cprob / num_open
        total = 0.0
        
        # Duyệt qua tất cả các vị trí trống để đặt ô 2 hoặc 4
        for pos in empty_positions:
            i, j = pos
            # Đặt ô 2 với xác suất 0.9
            new_board_2 = board.copy()
            new_board_2[i, j] = 2
            total += (self.score_move_node(tuple(map(tuple, new_board_2)), 
                                          prob_factor * 0.9, depth + 1, max_depth) * 0.9)
            
            # Đặt ô 4 với xác suất 0.1
            new_board_4 = board.copy()
            new_board_4[i, j] = 4
            total += (self.score_move_node(tuple(map(tuple, new_board_4)), 
                                          prob_factor * 0.1, depth + 1, max_depth) * 0.1)
        
        return total / num_open
    
    def score_move_node(self, board_tuple, cprob, depth, max_depth):
        best = 0.0
        board = np.array(board_tuple, dtype=np.int64)
        
        # Thử tất cả 4 nước đi (0: lên, 1: xuống, 2: trái, 3: phải)
        for move in range(4):
            new_board = self.execute_move(board, move)
            if not np.array_equal(new_board, board):  # Nếu nước đi thay đổi bàn cờ
                new_board_tuple = tuple(map(tuple, new_board))
                current_score = self.score_tilechoose_node(new_board_tuple, cprob, depth, max_depth)
                best = max(best, current_score)
        
        return best
    
    def expectimax(self, board, max_depth=3):
        best_score = -np.inf
        best_move = -1
        board = np.array(board, dtype=np.int64)
        
        # Thử tất cả các nước đi từ trạng thái ban đầu
        for move in range(4):
            new_board = self.execute_move(board, move)
            if not np.array_equal(new_board, board):
                new_board_tuple = tuple(map(tuple, new_board))
                score = self.score_tilechoose_node(new_board_tuple, 1.0, 1, max_depth)
                if score > best_score:
                    best_score = score
                    best_move = move
        
        return best_move

        
if __name__ == '__main__': 
    from puzzle import GameGrid
    from heuristic import Heuristic
    heuristic_obj = Heuristic([SCORE_MONOTONICITY_WEIGHT, SCORE_EMPTY_WEIGHT])
    optimizer = ExpectimaxOptimizer(heuristic_func=heuristic_obj)
    game = GameGrid(auto_move=True, expectimax_func=optimizer.expectimax, depth_limit=2)