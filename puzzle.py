from tkinter import Frame, Label, CENTER
import random
import logic
import constants as c
import time
from joblib import Parallel, delayed

def gen():
    return random.randint(0, c.GRID_LEN - 1)

def test_move(board, direction):
    board_copy = [row[:] for row in board]
    if direction == 0:
        board_copy, _, _ = logic.up(board_copy)
    elif direction == 1:
        board_copy, _, _ = logic.down(board_copy)
    elif direction == 2:
        board_copy, _, _ = logic.left(board_copy)
    elif direction == 3:
        board_copy, _, _ = logic.right(board_copy)
    return board_copy

class GameGrid(Frame):
    def __init__(self, auto_move=False, expectimax_func=None, depth_limit=None, silent=False):
        self.expectimax_func = expectimax_func
        self.silent = silent
        Frame.__init__(self)
        self.auto_move = auto_move
        self.depth_limit = depth_limit
        self.score = 0
        if not silent:
            self.grid()
            self.master.title('2048')
            self.master.bind("<Key>", self.key_down)
        self.commands = {
            c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right,
            c.KEY_UP_ALT1: logic.up,
            c.KEY_DOWN_ALT1: logic.down,
            c.KEY_LEFT_ALT1: logic.left,
            c.KEY_RIGHT_ALT1: logic.right,
            c.KEY_UP_ALT2: logic.up,
            c.KEY_DOWN_ALT2: logic.down,
            c.KEY_LEFT_ALT2: logic.left,
            c.KEY_RIGHT_ALT2: logic.right,
        }

        self.grid_cells = []
        self.score_label = None
        if not silent:
            self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        if not silent:
            self.update_grid_cells()
        
        self.game_result = None
        if self.auto_move and not silent:
            self.run_ai_loop()
        
        if not silent:
            self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE + 50)
        background.grid()

        self.score_label = Label(
            master=background,
            text=f"Score: {self.score}",
            bg=c.BACKGROUND_COLOR_GAME,
            fg="white",
            font=("Helvetica", 16, "bold"),
            height=2,
            width=20,
            justify=CENTER
        )
        self.score_label.grid(row=0, column=0, columnspan=c.GRID_LEN, pady=(10, 0))

        grid_frame = Frame(
            background,
            bg=c.BACKGROUND_COLOR_GAME,
            width=c.SIZE,
            height=c.SIZE
        )
        grid_frame.grid(row=1, column=0, columnspan=c.GRID_LEN, pady=(0, 10))

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    grid_frame,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2
                )
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        if not self.silent and self.score_label:
            self.score_label.configure(text=f"Score: {self.score}")
        if not self.silent:
            self.master.title(f'2048 - Score: {self.score}')
        self.update_idletasks()

    def move(self, key):
        self.matrix, done, move_score = self.commands[key](self.matrix)
        if done:
            self.score += move_score
            self.matrix = logic.add_two(self.matrix)
            self.history_matrixs.append(self.matrix)
            if not self.silent:
                self.update_grid_cells()
            game_state = logic.game_state(self.matrix)
            if game_state == 'win':
                self.game_result = 'win'
                if not self.silent:
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.quit()
            elif game_state == 'lose':
                self.game_result = 'lose'
                if not self.silent:
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    time.sleep(1)
                    self.quit()

    def key_down(self, event):
        key = event.keysym
        if key == c.KEY_QUIT:
            exit()
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            if not self.silent:
                self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.move(key)

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2
        
    def get_ai_move(self):
        possible_moves = [c.KEY_UP, c.KEY_DOWN, c.KEY_LEFT, c.KEY_RIGHT]
        if self.expectimax_func:
            move = possible_moves[self.expectimax_func(self.matrix, self.depth_limit)]
            return move
        return None

    def ai_play_step(self):
        ai_key = self.get_ai_move()
        if ai_key:
            self.move(ai_key)
            return True
        return False

    def run_ai_loop(self):
        if self.silent:
            # Chế độ không GUI: chạy vòng lặp trực tiếp
            while logic.game_state(self.matrix) not in ["win", "lose"]:
                if not self.ai_play_step():
                    break
        else:
            # Chế độ GUI: vòng lặp với self.update()
            while logic.game_state(self.matrix) not in ["win", "lose"]:
                if not self.ai_play_step():
                    break
                self.update()
                self.update_idletasks()

    def run_single_game(self):
        """Run a single game until completion and return the result, score, and max tile."""
        max_tile = 0
        while self.game_result is None:
            # Update max tile
            for row in self.matrix:
                max_tile = max(max_tile, max(row))
            if not self.ai_play_step():
                break
        # Final check for max tile
        for row in self.matrix:
            max_tile = max(max_tile, max(row))
        return self.game_result, self.score, max_tile

    def get_history(self):
        return self.history_matrixs
    
class GameSimulator:
    def __init__(self, num_games, expectimax_func, depth_limit):
        self.num_games = num_games
        self.expectimax_func = expectimax_func
        self.depth_limit = depth_limit
        self.wins = 0
        self.scores = []
        self.reached_2048 = 0
        self.reached_4096 = 0
        self.reached_8192 = 0
    def run_simulation(self):
        """Run the specified number of games and calculate win percentage, max score, average score,
        and percentages of reaching 2048 and 4096."""
        for i in range(self.num_games):
            print(f"Running game {i+1}/{self.num_games}")
            game = GameGrid(auto_move=True, expectimax_func=self.expectimax_func, 
                          depth_limit=self.depth_limit, silent=True)
            result, score, max_tile = game.run_single_game()
            print(f"Game {i+1} completed. Score: {score}, Max Tile: {max_tile}")
            self.scores.append(score)
            if max_tile >= 2048:
                self.reached_2048 += 1
                self.wins += 1
            if max_tile >= 4096:
                self.reached_4096 += 1
            game.destroy()

        win_percentage = (self.wins / self.num_games) * 100
        percentage_2048 = (self.reached_2048 / self.num_games) * 100
        percentage_4096 = (self.reached_4096 / self.num_games) * 100
        max_score = max(self.scores) if self.scores else 0
        avg_score = sum(self.scores) / len(self.scores) if self.scores else 0
        print(f"Played {self.num_games} games. Won {self.wins} times. "
              f"Win percentage: {win_percentage:.2f}%")
        print(f"Reached 2048: {self.reached_2048} times. Percentage: {percentage_2048:.2f}%")
        print(f"Reached 4096: {self.reached_4096} times. Percentage: {percentage_4096:.2f}%")
        print(f"Max score: {max_score}")
        print(f"Average score: {avg_score:.2f}")
        return win_percentage, max_score, avg_score, percentage_2048, percentage_4096
    
    def run_simulation_parallel(self, num_jobs=4):
        """Run the specified number of games in parallel using joblib and calculate 
        win percentage, max score, average score, and percentages of reaching 2048 and 4096."""
        
        def run_single_game():
            """Run a single game and return its score."""
            game = GameGrid(auto_move=True, expectimax_func=self.expectimax_func, 
                          depth_limit=self.depth_limit, silent=True)
            result, score, max_tile = game.run_single_game()
            game.destroy()
            return result, score, max_tile
        
        results = Parallel(n_jobs=num_jobs, backend='loky')(
            delayed(run_single_game)() for _ in range(self.num_games)
        )
        
        for result, score, max_tile in results:
            self.scores.append(score)
            if max_tile >= 2048:
                self.reached_2048 += 1
                self.wins += 1
            if max_tile >= 4096:
                self.reached_4096 += 1
            if max_tile >= 8192:
                self.reached_8192 += 1
        
        win_percentage = (self.wins / self.num_games) * 100
        percentage_2048 = (self.reached_2048 / self.num_games) * 100
        percentage_4096 = (self.reached_4096 / self.num_games) * 100
        percentage_8192 = (self.reached_8192 / self.num_games) * 100
        max_score = max(self.scores) if self.scores else 0
        avg_score = sum(self.scores) / len(self.scores) if self.scores else 0
        
        print(f"Played {self.num_games} games. Won {self.wins} times. "
              f"Win percentage: {win_percentage:.2f}%")
        print(f"Reached 2048: {self.reached_2048} times. Percentage: {percentage_2048:.2f}%")
        print(f"Reached 4096: {self.reached_4096} times. Percentage: {percentage_4096:.2f}%")
        print(f"Reached 8192: {self.reached_8192} times. Percentage: {percentage_8192:.2f}%")
        print(f"Max score: {max_score}")
        print(f"Average score: {avg_score:.2f}")
        
        return win_percentage, max_score, avg_score, percentage_2048, percentage_4096