
class EightPuzzle:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = [[0, 1, 2],
                           [3, 4, 5],
                           [6, 7, 8]]

    def is_goal(self, state):
          return state == self.goal_state


    def get_successors(self, state):
        zero_row, zero_col = self.find_digit(state,0)
        successors = []
        directions={
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }
        for direction, (row_change, col_change) in directions.items():
            new_row = zero_row + row_change
            new_col = zero_col + col_change

            if self.is_valid_move(new_row, new_col):
                new_state = self.swap_tiles(state, zero_row, zero_col, new_row, new_col)
                successors.append((new_state, direction))

        return successors


    def find_digit(self, state,number):
        for row in range(3):
            for col in range(3):
                if state[row][col] == number:
                    return row, col
        return None



    def is_valid_move(self, row, col):
        return 0 <= row < 3 and 0 <= col < 3


    def swap_tiles(self, state, row1, col1, row2, col2):
      new_state = [list(row) for row in state]
      new_state[row1][col1], new_state[row2][col2] = new_state[row2][col2], new_state[row1][col1]
      return new_state



    def misplaced_tiles(self, state):
        misplaced = 0
        for row in range(3):
            for col in range(3):
                if state[row][col] != self.goal_state[row][col]:
                    misplaced += 1
        return misplaced


    def  manhattan_distance(self, state):
      manhattan = 0
      for row in range(3):
          for col in range(3):
              if state[row][col] != self.goal_state[row][col]:
                  goal_row, goal_col = self.find_digit(self.goal_state, state[row][col])
                  manhattan += abs(row - goal_row) + abs(col - goal_col)
      return manhattan

    def custom_heuristic(self, state):
        misplaced = 0
        for row in range(3):
            for col in range(3):
                if state[row][col] != self.goal_state[row][col]:
                    goal_row, goal_col = self.find_digit(self.goal_state, state[row][col])
                    if goal_row!=row:
                        misplaced+=1
                    if goal_col!=col:
                        misplaced+=1
        return misplaced

def print_solution(path, moves):
    for step, (state, move) in enumerate(zip(path[1:], moves), 1):
        print(f"Step {step}: Move {move}")
        for row in state:
            print(row)
        print()

from collections import deque
def Uniform_cost_search(problem):
 steps=0
 frontier = deque([(problem.initial_state,[], [])])
 explored = set()
 while frontier:
    current_state, path,moves = frontier.popleft()
    if problem.is_goal(current_state):
         print_solution(path + [current_state], moves)
         return moves,steps

    state_tuple = tuple(tuple(row) for row in current_state)
    if state_tuple in explored:
            continue
    steps+=1
    explored.add(state_tuple)
    for successor, move in problem.get_successors(current_state):
        if tuple(tuple(row) for row in successor) not in explored:
          frontier.append((successor, path + [current_state],moves+[move]))

start_state = [[7, 2, 4], [5, 0, 6], [8, 3, 1]]
puzzle = EightPuzzle(start_state)
solution = Uniform_cost_search(puzzle)

if solution:
        print(f"Solution found in {len(solution[0])} moves.")
        print (f"Nodes visited: {(solution[1])} .")
else:
        print("No solution found.")

import heapq
def Best_first_search(puzzle, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic(puzzle.initial_state), puzzle.initial_state, [], []))
    explored = set()
    steps=0
    while frontier:
        _, current_state, path, moves = heapq.heappop(frontier)

        if puzzle.is_goal(current_state):
            print_solution(path + [current_state], moves)
            return moves,steps

        state_tuple = tuple(tuple(row) for row in current_state)
        if state_tuple in explored:
            continue
        explored.add(state_tuple)
        steps+=1
        for successor, move in puzzle.get_successors(current_state):
            if tuple(tuple(row) for row in successor) not in explored:
                heapq.heappush(frontier, (heuristic(successor), successor, path + [current_state], moves + [move]))


    return None

start_state = [[7, 2, 4], [5, 0, 6], [8, 3, 1]]
puzzle = EightPuzzle(start_state)
solution = Best_first_search(puzzle, puzzle.manhattan_distance)

if solution:
        print(f"Solution with manhattan distances found in {len(solution[0])} moves.")
        print (f"Nodes visited: {(solution[1])} .")
else:
        print("No solution found.")

start_state = [[7, 2, 4], [5, 0, 6], [8, 3, 1]]
puzzle = EightPuzzle(start_state)
solution = Best_first_search(puzzle, puzzle.misplaced_tiles)

if solution:
        print(f"Solution with misplaced tiles found in {len(solution[0])} moves.")
        print (f"Nodes visited: {(solution[1])} .")
else:
        print("No solution found.")

start_state = [[7, 2, 4], [5, 0, 6], [8, 3, 1]]
puzzle = EightPuzzle(start_state)
solution = Best_first_search(puzzle, puzzle.custom_heuristic)
#this heuristic is not admissible since it can overestimate the true cost of reaching the goal: it does not consider how far it is from the goal a tile could be 2 moves away from its spot but since its not in the right column nor row the a heuristic would still give it +2
if solution:
        print(f"Solution with h3 heuristic found in {len(solution[0])} moves.")
        print (f"Nodes visited: {(solution[1])} .")
else:
        print("No solution found.")

def astar_search(puzzle,heuristic):
   frontier = []
   heapq.heappush(frontier, (heuristic(puzzle.initial_state), 0, puzzle.initial_state, [], [])) # Because: f = g + h, where g = cost from start, h = heuristic
   explored = set()
   steps=0
   while frontier:
        f, g, current_state, path, moves = heapq.heappop(frontier)

        if puzzle.is_goal(current_state):
            print_solution(path + [current_state], moves)
            return moves,steps

        state_tuple = tuple(tuple(row) for row in current_state)
        if state_tuple in explored:
            continue
        explored.add(state_tuple)
        steps+=1
        for successor, move in puzzle.get_successors(current_state):
            if tuple(tuple(row) for row in successor) not in explored:
                g_cost = g + 1 # g_cost is the cost to reach this state (g + 1 because it's one move away since all moves are equal)
                f_cost = g_cost + heuristic(successor) # Because: f = g + h, where g = cost from start, h = heuristic
                heapq.heappush(frontier, (f_cost, g_cost, successor, path + [current_state], moves + [move]))

   return None

start_state = [[7, 2, 4], [5, 0, 6], [8, 3, 1]]
puzzle = EightPuzzle(start_state)
solution = astar_search(puzzle, puzzle.misplaced_tiles)

if solution:
        print(f"Solution with misplaced tiles found in {len(solution[0])} moves.")
        print (f"Nodes visited: {(solution[1])} .")
else:
        print("No solution found.")

start_state = [[7, 2, 4], [5, 0, 6], [8, 3, 1]]
puzzle = EightPuzzle(start_state)
solution = astar_search(puzzle, puzzle.manhattan_distance)

if solution:
        print(f"Solution with manhattan distance found in {len(solution[0])} moves.")
        print (f"Nodes visited: {(solution[1])} .")
else:
        print("No solution found.")

"""We notice that a* finds the optimal solution much faster (by visiting much fewer nodes) than the uniform cost search (which is the same as a breadth first search here since every move has the same cost)."""
