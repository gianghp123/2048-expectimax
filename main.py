
from Expectimaxoptimizer import ExpectimaxOptimizer
from puzzle import GameGrid
from heuristic import Heuristic

SCORE_LOST_PENALTY = 200000.0
SCORE_MONOTONICITY_POWER = 4.0
SCORE_MONOTONICITY_WEIGHT =10
SCORE_EMPTY_WEIGHT = 10


        
if __name__ == '__main__': 
    
    heuristic_obj = Heuristic([SCORE_MONOTONICITY_WEIGHT, SCORE_EMPTY_WEIGHT])
    optimizer = ExpectimaxOptimizer(heuristic_obj)
    game = GameGrid(auto_move=True, expectimax_func=optimizer.expectimax, depth_limit=2)