from puzzle import GameGrid
from heuristic import Heuristic
from expectimax_optimizer import ExpectimaxOptimizer      
if __name__ == '__main__': 
    from puzzle import GameGrid
    from heuristic import Heuristic
    heuristic_obj = Heuristic([7, 1200, 150])
    optimizer = ExpectimaxOptimizer(heuristic_func=heuristic_obj)
    game = GameGrid(auto_move=True, expectimax_func=optimizer.expectimax, depth_limit=2)