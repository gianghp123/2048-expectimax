import random
import constants as c

#######
# Task 1a #
#######

def new_game(n):
    matrix = []
    for i in range(n):
        matrix.append([0] * n)
    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix

###########
# Task 1b #
###########

def add_two(mat):
    a = random.randint(0, len(mat)-1)
    b = random.randint(0, len(mat)-1)
    while mat[a][b] != 0:
        a = random.randint(0, len(mat)-1)
        b = random.randint(0, len(mat)-1)
    x = random.random()
    mat[a][b] = 2 if x < 0.9 else 4
    return mat

###########
# Task 1c #
###########

def game_state(mat):
    # Check for win cell
    # for i in range(len(mat)):
    #     for j in range(len(mat[0])):
    #         if mat[i][j] == 2048:
    #             return 'win'
    # Check for any zero entries
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'
    # Check for same cells that touch each other
    for i in range(len(mat)-1):
        for j in range(len(mat[0])-1):
            if mat[i][j] == mat[i+1][j] or mat[i][j] == mat[i][j+1]:
                return 'not over'
    for k in range(len(mat)-1):  # Last row
        if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1):  # Last column
        if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'

###########
# Task 2a #
###########

def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

###########
# Task 2b #
###########

def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

##########
# Task 3 #
##########

def cover_up(mat):
    new = [[0] * c.GRID_LEN for _ in range(c.GRID_LEN)]
    done = False
    for i in range(c.GRID_LEN):
        count = 0
        for j in range(c.GRID_LEN):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done

def merge(mat, done):
    score = 0
    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN-1):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                score += mat[i][j]  # Cộng giá trị ô mới vào điểm số
                mat[i][j+1] = 0
                done = True
    return mat, done, score

def up(game):
    game = transpose(game)
    game, done = cover_up(game)
    game, done, score = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(game)
    return game, done, score

def down(game):
    game = reverse(transpose(game))
    game, done = cover_up(game)
    game, done, score = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(reverse(game))
    return game, done, score

def left(game):
    game, done = cover_up(game)
    game, done, score = merge(game, done)
    game = cover_up(game)[0]
    return game, done, score

def right(game):
    game = reverse(game)
    game, done = cover_up(game)
    game, done, score = merge(game, done)
    game = cover_up(game)[0]
    game = reverse(game)
    return game, done, score