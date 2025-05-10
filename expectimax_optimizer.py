import numpy as np
from puzzle import test_move

class ExpectimaxOptimizer:
    def __init__(self, heuristic_func):
        """Khởi tạo optimizer với hàm heuristic."""
        self.heuristic_func = heuristic_func
        self.heuristic_cache = {}      # Cache cho heuristic
        self.expectimax_cache = {}     # Cache cho nút Chance
        self.move_node_cache = {}      # Cache mới cho nút Player

    def score_heur_board(self, board_tuple):
        """Đánh giá bảng bằng hàm heuristic với caching."""
        if board_tuple in self.heuristic_cache:
            return self.heuristic_cache[board_tuple]
        board = np.array(board_tuple, dtype=np.int64)
        score = self.heuristic_func(board)
        self.heuristic_cache[board_tuple] = score
        return score
    
    def execute_move(self, board, move):
        """Thực hiện nước đi bằng hàm test_move."""
        return test_move(board, move)
    
    def score_tilechoose_node(self, board_tuple, cprob, depth, max_depth):
        """Đánh giá nút đặt ô với caching và cắt tỉa cải tiến."""
        cache_key = (board_tuple, depth)
        if cache_key in self.expectimax_cache:
            return self.expectimax_cache[cache_key]
        
        # Dừng sớm nếu xác suất quá thấp hoặc vượt quá độ sâu tối đa
        if cprob < 0.001 or depth >= max_depth:
            score = self.score_heur_board(board_tuple)
            self.expectimax_cache[cache_key] = score
            return score
        
        board = np.array(board_tuple, dtype=np.int64)
        empty_positions = np.argwhere(board == 0)
        if empty_positions.size == 0:
            self.expectimax_cache[cache_key] = 0.0
            return 0.0
        
        num_open = len(empty_positions)
        prob_factor = cprob / num_open
        total = 0.0
        
        # Cắt tỉa nhánh xác suất thấp khi có nhiều ô trống
        if num_open > 4 and prob_factor * 0.9 < 0.1:  # Tương tự mã gốc
            score = self.score_heur_board(board_tuple)
            self.expectimax_cache[cache_key] = score
            return score
        
        for pos in empty_positions:
            i, j = pos
            # Ô 2 với xác suất 0.9
            new_board_2 = board.copy()
            new_board_2[i, j] = 2
            new_board_2_tuple = tuple(map(tuple, new_board_2))
            score_2 = self.score_move_node(new_board_2_tuple, prob_factor * 0.9, depth + 1, max_depth)
            total += score_2 * 0.9
            
            # Ô 4 với xác suất 0.1
            new_board_4 = board.copy()
            new_board_4[i, j] = 4
            new_board_4_tuple = tuple(map(tuple, new_board_4))
            score_4 = self.score_move_node(new_board_4_tuple, prob_factor * 0.1, depth + 1, max_depth)
            total += score_4 * 0.1
        
        average_score = total / num_open
        self.expectimax_cache[cache_key] = average_score
        return average_score
    
    def score_move_node(self, board_tuple, cprob, depth, max_depth):
        """Đánh giá nút chọn nước đi với caching."""
        cache_key = (board_tuple, depth)
        if cache_key in self.move_node_cache:
            return self.move_node_cache[cache_key]
        
        best = 0.0
        board = np.array(board_tuple, dtype=np.int64)
        
        for move in range(4):
            new_board = self.execute_move(board, move)
            if not np.array_equal(new_board, board):
                new_board_tuple = tuple(map(tuple, new_board))
                current_score = self.score_tilechoose_node(new_board_tuple, cprob, depth, max_depth)
                best = max(best, current_score)
        
        self.move_node_cache[cache_key] = best
        return best
    
    def expectimax(self, board, max_depth=3):
        """Xác định nước đi tốt nhất bằng Expectimax."""
        best_score = -np.inf
        best_move = -1
        board = np.array(board, dtype=np.int64)
        
        for move in range(4):
            new_board = self.execute_move(board, move)
            if not np.array_equal(new_board, board):
                new_board_tuple = tuple(map(tuple, new_board))
                score = self.score_tilechoose_node(new_board_tuple, 1.0, 1, max_depth)
                if score > best_score:
                    best_score = score
                    best_move = move
        
        return best_move
