import copy

expanded_node_count = 0

# read from our input files
def read_two_grids(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f]

    grids = []
    current_grid = []

    for line in lines:
        if line == "":
            if current_grid:
                grids.append(current_grid)
                current_grid = []
        else:
            row = list(map(int, line.split()))
            current_grid.append(row)

    # append last grid if file doesn't end with blank line
    if current_grid:
        grids.append(current_grid)

    if len(grids) != 2:
        raise ValueError("Expected exactly two grids in input")

    return grids[0], grids[1]

def swap(input_grid, x, y, n_x, n_y):
    if n_x >= 0 and n_y >= 0 and n_x < 3 and n_y < 3:
        arr = copy.deepcopy(input_grid)
        temp = arr[x][y]
        arr[x][y] = arr[n_x][n_y]
        arr[n_x][n_y] = temp
        return arr
    return None

# takes in a state and returns all possible states
def make_future_states(input_grid):
    global expanded_node_count
    ret = []
    x = -1
    y = -1
    for i in range(0, 3):
        for j in range(0, 3):
            if input_grid[i][j] == 0:
                x = i
                y = j
                break

    # the x and y are switched up
    # 	sorry about that

    #up
    up = swap(input_grid, x, y, x - 1, y)
    if up is not None:
        ret.append(up)
        expanded_node_count += 1

    #down
    down = swap(input_grid, x, y, x + 1, y)
    if down is not None:
        ret.append(down)
        expanded_node_count += 1

    #left
    left = swap(input_grid, x, y, x, y - 1)
    if left is not None:
        ret.append(left)
        expanded_node_count += 1

    #right
    right = swap(input_grid, x, y, x, y + 1)
    if right is not None:
        ret.append(right)
        expanded_node_count += 1

    return ret

def find_val(val, goal_g):
    for i in range(0, 3):
        for j in range(0, 3):
            if val == goal_g[i][j]:
                return i, j

    return i, j

# computes the manhattan distance for each value in our puzzle
def compute_score(curr, goal_g):
    total_score = 0 
    for i in range(0, 3):
        for j in range(0, 3):
            val = curr[i][j]
            if val == 0:
                continue
            x, y = find_val(val, goal_g)
            total_score += abs(i - x) + abs(j - y)
    return total_score

# chooses the state with the best score
def compute_next_state(future_states, goal_g):
    scores = []
    indx = 0 
    best_idx = 0

    for arr in future_states:
        scores.append(compute_score(arr, goal_g))
        if scores[indx] < scores[best_idx]:
            best_idx = indx
        indx += 1

    return future_states[best_idx]

def A_star_iter(input_g, goal_g):
    #return an array of all future states
    future_states = make_future_states(input_g)

    #compute the scores for each future state
    #   distances
    #   return best score state
    next_state = compute_next_state(future_states, goal_g)

    return next_state 

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <input_file>")
        sys.exit(1)

    filename = sys.argv[1]
    input_grid, goal_grid = read_two_grids(filename)

    print("Input:")
    for row in input_grid:
        print(row)

    print("\nGoal:")
    for row in goal_grid:
        print(row)

    print()

    next_state = copy.deepcopy(input_grid)

    score = 99
    iteration = 1
    while score > 0:
         next_state = A_star_iter(next_state, goal_grid)
         score = compute_score(next_state, goal_grid)
         print()
         print("Step #" + str(iteration))
         for row in next_state:
             print(row)
         if iteration == 100: #early stop at 100
             exit()
         iteration += 1
         
    print("\nGoal:")
    for row in goal_grid:
        print(row)

    print("\nSolution:")
    for row in next_state:
        print(row)

    print("Generated nodes: " + str(expanded_node_count))
    print("Expanded nodes: " + str(iteration))

