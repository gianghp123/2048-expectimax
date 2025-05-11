import numpy as np

class Heuristic:
    def __init__(self, params, base_weight=200000.0):
        """Initialize heuristic with adjustable parameters."""
        self.params = params
        self.SCORE_MONOTONICITY_WEIGHT = params[0]  # Scale for optimization
        self.SCORE_EMPTY_WEIGHT = params[1]         # Scale for optimization
        self.SCORE_CORNER_WEIGHT = params[2]        # Scale for optimization
        self.base_weight = base_weight

    def _score_heur(self, board):
        """Compute the heuristic score for the entire 2048 board with debug prints."""
        total_monotonicity = 0.0
        total_empty = sum(1 for row in board for tile in row if tile == 0)

        for row in board:
            row_monotonicity = self.score_row(row)
            total_monotonicity += row_monotonicity

        transposed = list(zip(*board))
        for col in transposed:
            col_monotonicity = self.score_row(col)
            total_monotonicity += col_monotonicity

        # Corner bonus: Check if max tile is in any of the four corners
        max_tile_value = max(tile for row in board for tile in row)
        corner_bonus = 0.0
        if max_tile_value > 0 and (
            board[0][0] == max_tile_value or
            board[0][3] == max_tile_value or
            board[3][0] == max_tile_value or
            board[3][3] == max_tile_value
        ):
            corner_bonus = self.SCORE_CORNER_WEIGHT * np.log2(max_tile_value)

        # Tính các điểm thành phần
        empty_score = self.SCORE_EMPTY_WEIGHT * total_empty
        monotonicity_score = -self.SCORE_MONOTONICITY_WEIGHT * total_monotonicity

        print(f"Empty Score: {empty_score}")
        print(f"Monotonicity Score: {monotonicity_score}")
        print(f"Corner Bonus: {corner_bonus}")

        total_score = self.base_weight + empty_score + monotonicity_score + corner_bonus
        return total_score

    def score_row(self, row):
        """Compute monotonicity score for a single row or column."""
        monotonicity_left = 0.0
        monotonicity_right = 0.0
        monotonicity_power = 4.0

        ranks = [0 if tile == 0 else int(np.log2(tile)) for tile in row]

        for i in range(1, 4):
            if ranks[i - 1] > ranks[i]:
                monotonicity_left += ranks[i - 1] ** monotonicity_power - ranks[i] ** monotonicity_power
            else:
                monotonicity_right += ranks[i] ** monotonicity_power - ranks[i - 1] ** monotonicity_power

        monotonicity_score = min(monotonicity_left, monotonicity_right)
        return monotonicity_score

    def __call__(self, board):
        """Make the object callable, returning the heuristic score."""
        return self._score_heur(board)