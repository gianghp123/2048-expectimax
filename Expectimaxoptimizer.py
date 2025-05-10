import numpy as np
from puzzle import test_move
class ExpectimaxOptimizer:
    def __init__(self, heuristic_func): # Trả về điểm heuristic cho trạng thái hiện tại của bàn cờ
        """Khởi tạo trình tối ưu hóa với hàm heuristic."""
        self.heuristic_func = heuristic_func

    def score_heur_board(self, board): # copy 1 mảng mới và thử di chuyển theo các hướng 0,1,2,3
        """Đánh giá bảng bằng cách sử dụng hàm tìm kiếm được cung cấp."""
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
