import numpy as np
import copy
from collections import defaultdict
import time


# Adds fences from a list to the board
# Removes connections
def fence_addition(b, fences):

    for fen in fences:
        row = int(fen[1])
        col = ord(fen[0]) - 64
        dir = fen[2]   #direction

        neigh = '-'

        if dir == 'h':
            curr = chr(col + 64) + str(row)

            neigh = chr(col + 65) + str(row)

            block_up = chr(col + 64) + str(row + 1)

            block_up_neigh = chr(col + 65) + str(row + 1)

            if (block_up in b[curr]):
                b[curr].remove(block_up)
            if (block_up_neigh in b[neigh]):
                b[neigh].remove(block_up_neigh)

            if (curr in b[block_up]):
                b[block_up].remove(curr)
            if (neigh in b[block_up_neigh]):
                b[block_up_neigh].remove(neigh)

        if dir == 'v':
            curr = chr(col + 64) + str(row)

            neigh = chr(col + 64) + str(row + 1)

            block_right = chr(col + 65) + str(row)

            block_right_neigh = chr(col + 65) + str(row + 1)

            if (block_right in b[curr]):
                b[curr].remove(block_right)
            if (block_right_neigh in b[neigh]):
                b[neigh].remove(block_right_neigh)

            if (curr in b[block_right]):
                b[block_right].remove(curr)
            if (neigh in b[block_right_neigh]):
                b[block_right_neigh].remove(neigh)

    return b


# Finds all the valid piece moves a player can make
def possible_piece(board, side, player1, player2):

    potential_piece = []

    if side == 1:
        pos = player1
        op_pos = player2
    else:
        pos = player2
        op_pos = player1

    potential_piece.extend(board[pos])

    if op_pos in potential_piece:
        potential_piece.remove(op_pos)
            
        add_pos = ''

        row = int(pos[1])
        col = ord(pos[0]) - 64

        row_o = int(op_pos[1])
        col_o = ord(op_pos[0]) - 64

        if (row == row_o):
            if (col_o < col):
                add_pos = chr(col_o - 1 + 64) + str(row)
            else:
                add_pos = chr(col_o + 1 + 64) + str(row)

            if (add_pos not in board[op_pos]):
                potential_piece.extend(board[op_pos])
                if pos in potential_piece:
                    potential_piece.remove(pos)
            else:
                potential_piece.append(add_pos)
                    
        else:
            if (row_o < row):
                add_pos = chr(col_o + 64) + str(row_o - 1)
            else:
                add_pos = chr(col_o + 64) + str(row_o + 1)

            if (add_pos not in board[op_pos]):
                potential_piece.extend(board[op_pos])
                if pos in potential_piece:
                    potential_piece.remove(pos)
            else:
                potential_piece.append(add_pos)

    return potential_piece


# Checks if each player has a path to goal using BFS
def path_check(graph, start, goal):
    explored = []
     
    # Queue for traversing the graph in the BFS
    queue = [[start]]
     
    # If the desired node is reached
    if start in goal:
        return True
     
    # Loop to traverse the graph with the help of the queue
    while queue:
        path = queue.pop(0)
        node = path[-1]
         
        # Condition to check if the current node is not visited
        if node not in explored:
            neighbours = graph[node]
             
            # Loop to iterate over the neighbours of the node
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                 
                # Condition to check if the neighbour node is the goal
                if neighbour in goal:
                    return True
            explored.append(node)
 
    # Condition when the nodes are not connected
    return False


# Finds all the valid fence positions at which a fence may be placed
def possible_fence(board, curr_fences, player1, player2):

    potential_fences = []

    for c in range(1, 9):
        for r in range(1,9):

            pos = chr(c + 64) + str(r)

            if  (pos + 'h') in curr_fences or (pos + 'v') in curr_fences:
                continue

            nei = chr(c + 65) + str(r)

            pos_up = chr(c + 64) + str(r + 1)
            nei_up = chr(c + 65) + str(r + 1)

            if (pos_up in board[pos] and nei_up in board[nei]):
                potential_fences.append(pos + 'h')
                
                b_temp = copy.deepcopy(board)
                
                b_temp = fence_addition(b_temp, [pos + 'h'])

                if (path_check(b_temp, player1, ['A9','B9','C9','D9','E9','F9','G9','H9','I9'])==False or path_check(b_temp, player2, ['A1','B1','C1','D1','E1','F1','G1','H1','I1'])==False):
                    potential_fences.remove(pos + 'h')

            if (nei in board[pos] and nei_up in board[pos_up]):
                potential_fences.append(pos + 'v')
                
                b_temp = copy.deepcopy(board)
                
                b_temp = fence_addition(b_temp, [pos + 'v'])

                if (path_check(b_temp, player1, ['A9','B9','C9','D9','E9','F9','G9','H9','I9'])==False or path_check(b_temp, player2, ['A1','B1','C1','D1','E1','F1','G1','H1','I1'])==False):
                    potential_fences.remove(pos + 'v')

    return potential_fences


# Executes a piece move
def piece_move(move, board, side_to_play, player1, player2):
    
    if side_to_play == 1:
        player1 = move
        side_to_play = 2

    else:
        player2 = move
        side_to_play = 1

    return board, side_to_play, player1, player2


# Executes a fence move
def fence_move(move, board, curr_fences, side_to_play, player1_fen_rem, player2_fen_rem):

    if side_to_play == 1:
        board = fence_addition(board, [move])
        curr_fences.append(move)
        side_to_play = 2
        player1_fen_rem -= 1

    else:
        board = fence_addition(board, [move])
        curr_fences.append(move)
        side_to_play = 1
        player2_fen_rem -= 1
        
    return board, curr_fences, side_to_play, player1_fen_rem, player2_fen_rem


# Gives the minimum number of moves a player needs to get to goal
def BFS_score(graph, start, goal):
    explored = []
     
    # Queue for traversing the graph in the BFS
    queue = [[start]]

    if start in goal:
        return 0
     
    # Loop to traverse the graph with the help of the queue
    while queue:
        path = queue.pop(0)
        node = path[-1]
         
        # Condition to check if the current node is not visited
        if node not in explored:
            neighbours = graph[node]
             
            # Loop to iterate over the neighbours of the node
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                 
                # Condition to check if the neighbour node is the goal
                if neighbour in goal:
                    new_path.pop(0)
                    return len(new_path)
            explored.append(node)
 
    # Condition when the nodes are not connected
    return 1000000000


# MCTS class
# state: represents the board state (dictionary)
# parent: None for the root node and for other nodes it is equal to the node it is derived from
# children: contains all expanded actions from the current node
# parent_action: None for the root node and for other nodes it is equal to the action which it’s parent carried out.
# _number_of_visits: number of times current node is visited
# _untried_actions: represents the list of all possible actions not yet expanded
class MonteCarloTreeSearchNode():
    def __init__(self, state, curr_fences, side_to_play, player1, player1_fen_rem,  player2, player2_fen_rem, parent=None, parent_action=None):
        self.state = state
        self.curr_fences = curr_fences
        self.side_to_play = side_to_play
        self.player1 = player1
        self.player1_fen_rem = player1_fen_rem
        self.player2 = player2
        self.player2_fen_rem = player2_fen_rem
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        # print(self.state)
        return
    
    # Creates a list of all untried actions for a given state
    def untried_actions(self):

        self._untried_actions = self.get_legal_actions()
        return self._untried_actions

    # Returns score of node
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    # Returns number of times node was visited
    def n(self):
        return self._number_of_visits

    # Expands node by choosing one of its untried actions
    def expand(self):
	
        action = self._untried_actions.pop()
        child_node = self.move(action)

        self.children.append(child_node)
        return child_node 

    # Checks for terminal node
    def is_terminal_node(self):
        return self.is_game_over()

    # Simulates game play, until game is over or 50 moves have been played
    def rollout(self):
        current_rollout_state = self

        r = 50
        
        while not current_rollout_state.is_game_over() and r != 0:
            
            possible_moves = current_rollout_state.get_legal_actions()
            
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
            r -= 1

        return current_rollout_state.game_result()

    # Back propgates result up the tree
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    # Checks if all untired actions have been expanded
    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    # Selects best child of parent using UCT with c = 2
    def best_child(self, c_param):
        
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    # The rollout selects a random move
    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    # Selection phase, we choose which node to explore at
    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child(c_param=2)
        return current_node

    # Main Function
    # 4 Phases run here
    def best_action(self):
        simulation_no = len(self._untried_actions) * 2 # Runs for 2 times the number of untried actions
        
        
        for i in range(simulation_no):
            
            v = self._tree_policy()
            
            reward = v.rollout()
            
            v.backpropagate(reward)
        
        return self.best_child(c_param=2)

    # list of all possible actions from current state
    def get_legal_actions(self): 
        
        potential_moves = []

        if self.side_to_play == 1 and self.player1_fen_rem != 0:
            potential_moves.extend(possible_fence(self.state, self.curr_fences, self.player1, self.player2))
        elif self.side_to_play == 2 and self.player2_fen_rem != 0:
            potential_moves.extend(possible_fence(self.state, self.curr_fences, self.player1, self.player2))

        potential_moves.extend(possible_piece(self.state, self.side_to_play, self.player1, self.player2))

        return potential_moves
    
    # Checks if game is finished or not
    def is_game_over(self):
        
        if (self.player1[1] == '9' or self.player2[1] == '1'):
            return True
        
        return False
    
    # Returns result of game
    def game_result(self):
        
        player1_score = BFS_score(self.state, self.player1, ['A9','B9','C9','D9','E9','F9','G9','H9','I9'])
    
        player2_score = BFS_score(self.state, self.player2, ['A1','B1','C1','D1','E1','F1','G1','H1','I1'])
        
        raw_score = 0

        if player1_score == 0:
            raw_score = -1
        if player2_score == 0:
            raw_score = 1

        return -1 * raw_score
        
    # Executes move and returns new node
    def move(self,action):
        
        cnode = copy.deepcopy(self)

        if (len(action) == 2):
            board, side_to_play, player1, player2 = piece_move(action, cnode.state, cnode.side_to_play, cnode.player1, cnode.player2)

            del cnode
            node = MonteCarloTreeSearchNode(
                            board, self.curr_fences, side_to_play, 
                            player1, self.player1_fen_rem, 
                            player2, self.player2_fen_rem,
                            parent=self, parent_action=action)

            return node
        
        else:
            board, curr_fences, side_to_play, player1_fen_rem, player2_fen_rem = fence_move(action, cnode.state, cnode.curr_fences, cnode.side_to_play,
                                                                                            cnode.player1_fen_rem, cnode.player2_fen_rem)
            
            del cnode
            node = MonteCarloTreeSearchNode(
                            board, curr_fences, side_to_play, 
                            self.player1, player1_fen_rem, 
                            self.player2, player2_fen_rem,
                            parent=self, parent_action=action)
            
            return node


# Input -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> 
inp = input()

game = inp.split()

# PLayer positions
positions = game[0].split("/")

player1_pos = positions[0]
player2_pos = positions[1]

# Current board fences
if (game[1] == "None"):
    fences = []
else:
    fences = game[1].split("/")

# Player to make move
side_to_play = int(game[2])

# Player fences reamining
fences_remaining = game[3].split("/")

player1_fen_rem = int(fences_remaining[0])
player2_fen_rem = int(fences_remaining[1])

# Board -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> 

b = {'A1': ['A2', 'B1'],
        'A2': ['A1', 'A3', 'B2'],
        'A3': ['A2', 'A4', 'B3'],
        'A4': ['A3', 'A5', 'B4'],
        'A5': ['A4', 'A6', 'B5'],
        'A6': ['A5', 'A7', 'B6'],
        'A7': ['A6', 'A8', 'B7'],
        'A8': ['A7', 'A9', 'B8'],
        'A9': ['A8', 'B9'],

        'B1': ['A1', 'B2', 'C1'],
        'B2': ['A2', 'B1', 'B3', 'C2'],
        'B3': ['A3', 'B2', 'B4', 'C3'],
        'B4': ['A4', 'B3', 'B5', 'C4'],
        'B5': ['A5', 'B4', 'B6', 'C5'],
        'B6': ['A6', 'B5', 'B7', 'C6'],
        'B7': ['A7', 'B6', 'B8', 'C7'],
        'B8': ['A8', 'B7', 'B9', 'C8'],
        'B9': ['A9', 'B8', 'C9'],

        'C1': ['B1', 'C2', 'D1'],
        'C2': ['B2', 'C1', 'C3', 'D2'],
        'C3': ['B3', 'C2', 'C4', 'D3'],
        'C4': ['B4', 'C3', 'C5', 'D4'],
        'C5': ['B5', 'C4', 'C6', 'D5'],
        'C6': ['B6', 'C5', 'C7', 'D6'],
        'C7': ['B7', 'C6', 'C8', 'D7'],
        'C8': ['B8', 'C7', 'C9', 'D8'],
        'C9': ['B9', 'C8', 'D9'],
        
        'D1': ['C1', 'D2', 'E1'],
        'D2': ['C2', 'D1', 'D3', 'E2'],
        'D3': ['C3', 'D2', 'D4', 'E3'],
        'D4': ['C4', 'D3', 'D5', 'E4'],
        'D5': ['C5', 'D4', 'D6', 'E5'],
        'D6': ['C6', 'D5', 'D7', 'E6'],
        'D7': ['C7', 'D6', 'D8', 'E7'],
        'D8': ['C8', 'D7', 'D9', 'E8'],
        'D9': ['C9', 'D8', 'E9'],
        
        'E1': ['D1', 'E2', 'F1'],
        'E2': ['D2', 'E1', 'E3', 'F2'],
        'E3': ['D3', 'E2', 'E4', 'F3'],
        'E4': ['D4', 'E3', 'E5', 'F4'],
        'E5': ['D5', 'E4', 'E6', 'F5'],
        'E6': ['D6', 'E5', 'E7', 'F6'],
        'E7': ['D7', 'E6', 'E8', 'F7'],
        'E8': ['D8', 'E7', 'E9', 'F8'],
        'E9': ['D9', 'E8', 'F9'],
        
        'F1': ['E1', 'F2', 'G1'],
        'F2': ['E2', 'F1', 'F3', 'G2'],
        'F3': ['E3', 'F2', 'F4', 'G3'],
        'F4': ['E4', 'F3', 'F5', 'G4'],
        'F5': ['E5', 'F4', 'F6', 'G5'],
        'F6': ['E6', 'F5', 'F7', 'G6'],
        'F7': ['E7', 'F6', 'F8', 'G7'],
        'F8': ['E8', 'F7', 'F9', 'G8'],
        'F9': ['E9', 'F8', 'G9'],
        
        'G1': ['F1', 'G2', 'H1'],
        'G2': ['F2', 'G1', 'G3', 'H2'],
        'G3': ['F3', 'G2', 'G4', 'H3'],
        'G4': ['F4', 'G3', 'G5', 'H4'],
        'G5': ['F5', 'G4', 'G6', 'H5'],
        'G6': ['F6', 'G5', 'G7', 'H6'],
        'G7': ['F7', 'G6', 'G8', 'H7'],
        'G8': ['F8', 'G7', 'G9', 'H8'],
        'G9': ['F9', 'G8', 'H9'],
        
        'H1': ['G1', 'H2', 'I1'],
        'H2': ['G2', 'H1', 'H3', 'I2'],
        'H3': ['G3', 'H2', 'H4', 'I3'],
        'H4': ['G4', 'H3', 'H5', 'I4'],
        'H5': ['G5', 'H4', 'H6', 'I5'],
        'H6': ['G6', 'H5', 'H7', 'I6'],
        'H7': ['G7', 'H6', 'H8', 'I7'],
        'H8': ['G8', 'H7', 'H9', 'I8'],
        'H9': ['G9', 'H8', 'I9'],
        
        'I1': ['H1', 'I2'],
        'I2': ['H2', 'I1', 'I3'],
        'I3': ['H3', 'I2', 'I4'],
        'I4': ['H4', 'I3', 'I5'],
        'I5': ['H5', 'I4', 'I6'],
        'I6': ['H6', 'I5', 'I7'],
        'I7': ['H7', 'I6', 'I8'],
        'I8': ['H8', 'I7', 'I9'],
        'I9': ['H9', 'I8']}

b = fence_addition(b, fences)

# Output -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> ->

root = MonteCarloTreeSearchNode(state = b, curr_fences = fences, side_to_play=side_to_play,
                                player1=player1_pos, player1_fen_rem=player1_fen_rem,
                                player2=player2_pos, player2_fen_rem=player2_fen_rem)

start = time.time()
selected_node = root.best_action()
end = time.time()

ss_time_elapsed = end - start

# Print the move and the time elapsed in seconds
print(f"{selected_node.parent_action} {ss_time_elapsed:.6f}")