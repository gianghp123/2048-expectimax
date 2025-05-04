import numpy as np

class Heuristic:
    def __init__(self, params):
        """Initialize heuristic with adjustable parameters."""
        self.params = params
        self.SCORE_MONOTONICITY_WEIGHT = params[0] * 10  # Scale for optimization
        self.SCORE_EMPTY_WEIGHT = params[1] * 1000       # Scale for optimization

    def _score_heur(self, board_tuple):
        """Compute the heuristic score for the entire 2048 board with caching."""
        row_scores = sum(self.score_row(row) for row in board_tuple)
        transposed = tuple(zip(*board_tuple))
        col_scores = sum(self.score_row(col) for col in transposed)
        total_score = row_scores + col_scores
        return total_score

    def score_row(self, row):
        """Compute heuristic score for a single row or column."""
        empty = 0
        monotonicity_left = 0.0
        monotonicity_right = 0.0
        ranks = [0 if tile == 0 else int(np.log2(tile)) for tile in row]
        for rank in ranks:
            if rank == 0:
                empty += 1
        for i in range(1, 4):
            if ranks[i-1] > ranks[i]:
                monotonicity_left += ranks[i-1] ** 4.0 - ranks[i] ** 4.0
            else:
                monotonicity_right += ranks[i] ** 4.0 - ranks[i-1] ** 4.0
        score = (200000.0 +
                 self.SCORE_EMPTY_WEIGHT * empty -
                 self.SCORE_MONOTONICITY_WEIGHT * min(monotonicity_left, monotonicity_right))
        return score

    def __call__(self, board):
        """Make the object callable, converting board to tuple for caching."""
        board_tuple = tuple(map(tuple, board))
        return self._score_heur(board_tuple)