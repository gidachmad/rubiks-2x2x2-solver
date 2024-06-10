import time 
from collections import deque
import os
from tqdm import tqdm
import json

# Define the solved state
SOLVED_STATE = "YYYYBBBBRRRRGGGGOOOOWWWW"

# Define the moves affecting the string representation
# cube representation
#      0  1
#      2  3
# 4 5  8  9 12 13 16 17
# 6 7 10 11 14 15 18 19
#     20 21
#     22 23
MOVES = {
    "U":  [0, 2, 3, 1, 4, 5, 8, 9, 12, 13, 16, 17],
    "U'": [0, 1, 3, 2, 17, 16, 13, 12, 9, 8, 5, 4],
    "U2": [0, 2, 3, 1, 4, 5, 8, 9, 12, 13, 16, 17],
    "D": [20, 22, 23, 21, 19, 18, 15, 14, 11, 10, 7, 6],
    "D'": [20, 21, 23, 22, 6, 7, 10, 11, 14, 15, 18, 19],
    "D2": [20, 22, 23, 21, 19, 18, 15, 14, 11, 10, 7, 6],
    "F":  [8, 10, 11, 9, 5, 7, 20, 21, 14, 12, 3, 2],
    "F'": [8, 9, 11, 10, 2, 3, 12, 14, 21, 20, 7, 5],
    "F2": [8, 10, 11, 9, 5, 7, 20, 21, 14, 12, 3, 2],
    "B":  [16, 18, 19, 17, 6, 4, 0, 1, 13, 15, 23, 22],
    "B'": [16, 17, 19, 18, 22, 23, 15, 13, 1, 0, 4, 6],
    "B2": [16, 18, 19, 17, 6, 4, 0, 1, 13, 15, 23, 22],
    "L":  [4, 6, 7, 5, 17, 19, 22, 20, 10, 8, 2, 0],
    "L'": [4, 5, 7, 6, 0, 2, 8, 10, 20, 22, 19, 17],
    "L2": [4, 6, 7, 5, 17, 19, 22, 20, 10, 8, 2, 0],
    "R":  [12, 14, 15, 13, 1, 3, 9, 11, 21, 23, 18, 16],
    "R'": [12, 13, 15, 14, 16, 18, 23, 21, 11, 9, 3, 1],
    "R2": [12, 14, 15, 13, 1, 3, 9, 11, 21, 23, 18, 16],
}

REVERSE_MOVES = {
    "U": "U'", "U'": "U", "U2": "U2",
    "F": "F'", "F'": "F", "F2": "F2",
    "R": "R'", "R'": "R", "R2": "R2",
    "D": "D'", "D'": "D", "D2": "D2",
    "L": "L'", "L'": "L", "L2": "L2",
    "B": "B'", "B'": "B", "B2": "B2",
}

def rotate(state, indices):
    new_state = list(state)
    # rotate face
    for i in range(4):
        new_state[indices[i]] = state[indices[(i+1) % 4]]
    # rotate edges
    for i in range(8):
        new_state[indices[i + 4]] = state[indices[(i+2) % 8 + 4]]
    return "".join(new_state)

def rotate_front_back(state, indices):
    new_state = list(state)
    for i in range(4):
        new_state[indices[i]] = state[indices[(i+1) % 4]]
    for i in range(8):
        new_state[indices[i + 4]] = state[indices[(i+10) % 8 + 4]]
    return "".join(new_state)

def rotate_left_right(state, indices):
    new_state = list(state)
    for i in range(4):
        new_state[indices[i]] = state[indices[(i+1) % 4]]
    for i in range(8):
        new_state[indices[i + 4]] = state[indices[(i+10) % 8 + 4]]
    return "".join(new_state)



# Apply a move to the cube's string state
def apply_move(state, move):
    if move.endswith("2"):
        indices = MOVES[move[:-1]]
        state = rotate(state, indices)
    indices = MOVES[move]
    return rotate(state, indices)




# Check if the state is solved
def is_solved(state):
    return state == SOLVED_STATE

# Backtracking solver
def solve_cube_backtrack(state, depth, max_depth, path):
    shortest_path = None
    if is_solved(state):
        return path

    if depth == max_depth:
        return None

    for move in MOVES:
        new_state = apply_move(state, move)
        result = solve_cube_backtrack(new_state, depth + 1, max_depth, path + [move])
        if result:
            if not shortest_path or len(result) < len(shortest_path):
                shortest_path = result

    return shortest_path

# cube representation
#      0  1
#      2  3
# 4 5  8  9 12 13 16 17
# 6 7 10 11 14 15 18 19
#     20 21
#     22 23

def rotate_x(top, left, front, right, back, bottom):
    # front, left, bottom, right, top, back
    return "".join(front) + "".join(left) + "".join(bottom) + "".join(right) + "".join(top) + "".join(back)

def rotate_y(top, left, front, right, back, bottom):
    # top, front, right back, left, bottom
    return "".join(top) + "".join(front) + "".join(right) + "".join(back) + "".join(left) + "".join(bottom)
    
def rotate_z(top, left, front, right, back, bottom):
    # left, bottom, front, top, back, right
    return "".join(left) + "".join(bottom) + "".join(front) + "".join(top) + "".join(back) + "".join(right)

def get_face_to_rotate(state):
    # top = state[:4] left = state[4:8] front = state[8:12] right = state[12:16] back = state[16:20] bottom = state[20:24]
    return state[:4], state[4:8], state[8:12], state[12:16], state[16:20], state[20:24]


def apply_rotations(state):
    # divide cube into 6 faces
    rotations = list()
    for _ in range(4):
        state = rotate_x(*get_face_to_rotate(state))
        rotations.append(state)
        for _ in range(4):
            state = rotate_y(*get_face_to_rotate(state))
            rotations.append(state)
            for _ in range(4):
                state = rotate_z(*get_face_to_rotate(state))
                rotations.append(state)

    return rotations


def canonical_form(state):
    rotations = apply_rotations(state)
    return min(rotations)

def precompute_states():
    dp = {}
    queue = deque([(SOLVED_STATE, [])])
    dp[canonical_form(SOLVED_STATE)] = []

    # Correct upper limit for progress tracking
    total_states = 3_674_160
    # total_states = 100
    visited = set()
    visited.add(canonical_form(SOLVED_STATE))

    with tqdm(total=total_states, desc="Precomputing states") as pbar:
        while queue and len(dp) < total_states:
            current_state, path = queue.popleft()

            for move in MOVES:
                new_state = apply_move(current_state, move)
                canonical_new = canonical_form(new_state)
                if canonical_new not in visited:
                    dp[canonical_new] = path + [move]
                    visited.add(canonical_new)
                    queue.append((new_state, path + [move]))
                    pbar.update(1)
    
    return dp


def solve_dp(state, dp):
    canonical_state = canonical_form(state)
    return dp.get(canonical_state, None)


# Example usage
initial_state = "YYYYBBBBRRRRGGGGOOOOWWWW"

# Scramble the cube
# scrambled_state = apply_move(initial_state, "D")
scrambled_state = apply_move(initial_state, "U2")
# scrambled_state = apply_move(scrambled_state, "L")
scrambled_state = apply_move(scrambled_state, "R")
scrambled_state = apply_move(scrambled_state, "B'")
# scrambled_state = apply_move(scrambled_state, "L'")
scrambled_state = apply_move(scrambled_state, "F2")
scrambled_state = apply_move(scrambled_state, "R")
print("Scrambled state:", scrambled_state)
scrambled_state_backtrack = scrambled_state
scrambled_state_dp = scrambled_state

print("-------------------- Backtrack -------------------")
# Solve the scrambled cube
max_depth = 5 # Adjust based on the complexity of the scramble
start_backtrack = time.time()
solution_backtrack = solve_cube_backtrack(scrambled_state_backtrack, 0, max_depth, [])
end_backtrack = time.time()
print("Solution backtrack:", solution_backtrack)
print("Backtrack Time: ", (end_backtrack - start_backtrack))

# print final state after applying moves in solution_backtrack
print("initial state backtrack:", scrambled_state_backtrack)
for move in solution_backtrack:
    scrambled_state_backtrack = apply_move(scrambled_state_backtrack, move)
print("final state backtrack:", scrambled_state_backtrack)


print("-------------------- Dynamic Programming -------------------")
# if there is dp in file with json extension then load it, else compute it
if os.path.exists("dp.json"):
    with open("dp.json") as f:
        dp = json.load(f)
else:
    start_dp = time.time()
    dp = precompute_states()
    end_dp = time.time()
    print("DP Time: ", (end_dp - start_dp))
    with open("dp.json", "w") as f:
        json.dump(dp, f)

# Solve the scrambled cube using the precomputed DP table
start_dp = time.time()
solution_dp = solve_dp(scrambled_state_dp, dp)
end_dp = time.time()

# change the order of moves, and change move in solution_dp to reverse move
solution_dp = solution_dp[::-1]
for move in solution_dp:
    solution_dp[solution_dp.index(move)] = REVERSE_MOVES[move]

print("Solution DP:", solution_dp)
print("DP Time: ", (end_dp - start_dp))
print("initial state DP:", scrambled_state_dp)
for move in solution_dp:
    scrambled_state_dp = apply_move(scrambled_state_dp, move)

print("final state DP:", scrambled_state_dp)