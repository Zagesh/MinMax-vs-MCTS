import subprocess
import copy

# GAME MANAGER (GM)
# CLASS AND GAME FUNCTIONS SAME AS MIN-MAX AND MCTS
# DONE SO THAT THE GAME MANAGER CAN KEEP TRACK OF GAME STATE
# THE RELEVANT GAME STATE CAN THEN BE SENT TO TH ERELEVANT AGENT

class Board:
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
    
    def __init__(self, side_to_play, player1, player1_fen_rem,  player2, player2_fen_rem):
        self.side_to_play = side_to_play
        self.player1 = player1
        self.player1_fen_rem = player1_fen_rem
        self.player2 = player2
        self.player2_fen_rem = player2_fen_rem

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

def possible_piece(board):

    potential_piece = []

    if board.side_to_play == 1:
        pos = board.player1
        op_pos = board.player2
    else:
        pos = board.player2
        op_pos = board.player1

    potential_piece.extend(board.b[pos])

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

            if (add_pos not in board.b[op_pos]):
                potential_piece.extend(board.b[op_pos])
                if pos in potential_piece:
                    potential_piece.remove(pos)
            else:
                potential_piece.append(add_pos)
                    
        else:
            if (row_o < row):
                add_pos = chr(col_o + 64) + str(row_o - 1)
            else:
                add_pos = chr(col_o + 64) + str(row_o + 1)

            if (add_pos not in board.b[op_pos]):
                potential_piece.extend(board.b[op_pos])
                if pos in potential_piece:
                    potential_piece.remove(pos)
            else:
                potential_piece.append(add_pos)

    return potential_piece

def possible_fence(board, curr_fences):

    potential_fences = []

    for c in range(1, 9):
        for r in range(1,9):

            pos = chr(c + 64) + str(r)

            if  (pos + 'h') in curr_fences or (pos + 'v') in curr_fences:
                continue

            nei = chr(c + 65) + str(r)

            pos_up = chr(c + 64) + str(r + 1)
            nei_up = chr(c + 65) + str(r + 1)

            if (pos_up in board.b[pos] and nei_up in board.b[nei]):
                potential_fences.append(pos + 'h')
                
                b_temp = copy.deepcopy(board.b)
                
                b_temp = fence_addition(b_temp, [pos + 'h'])

                if (path_check(b_temp, board.player1, ['A9','B9','C9','D9','E9','F9','G9','H9','I9'])==False or path_check(b_temp, board.player2, ['A1','B1','C1','D1','E1','F1','G1','H1','I1'])==False):
                    potential_fences.remove(pos + 'h')

            if (nei in board.b[pos] and nei_up in board.b[pos_up]):
                potential_fences.append(pos + 'v')
                
                b_temp = copy.deepcopy(board.b)
                
                b_temp = fence_addition(b_temp, [pos + 'v'])

                if (path_check(b_temp, board.player1, ['A9','B9','C9','D9','E9','F9','G9','H9','I9'])==False or path_check(b_temp, board.player2, ['A1','B1','C1','D1','E1','F1','G1','H1','I1'])==False):
                    potential_fences.remove(pos + 'v')

    return potential_fences

def possible_move(board, curr_fences):

    potential_moves = []

    potential_moves.extend(possible_piece(board))

    if board.side_to_play == 1 and board.player1_fen_rem != 0:
        potential_moves.extend(possible_fence(board, curr_fences))
    elif board.side_to_play == 2 and board.player2_fen_rem != 0:
        potential_moves.extend(possible_fence(board, curr_fences))

    return potential_moves

def piece_move(move, board):
    
    if board.side_to_play == 1:
        board.player1 = move
        board.side_to_play = 2

    else:
        board.player2 = move
        board.side_to_play = 1

    return board

def fence_move(move, board, curr_fences):

    if board.side_to_play == 1:
        board.b = fence_addition(board.b, [move])
        curr_fences.append(move)
        board.side_to_play = 2
        board.player1_fen_rem -= 1

    else:
        board.b = fence_addition(board.b, [move])
        curr_fences.append(move)
        board.side_to_play = 1
        board.player2_fen_rem -= 1
        
    return board, curr_fences

def make_move(move, board, curr_fences):

    if move not in possible_move(board, curr_fences):
        return board, curr_fences

    if (len(move) == 2):
        board = piece_move(move, board)
    else:
        board, curr_fences = fence_move(move, board, curr_fences)

    return board, curr_fences

def gameOver(board):

    if (board.player1[1] == '9' or board.player2[1] == '1'):
        return True
    
    return False



# Input -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> 
inp = 'E1/E9 None 1 10/10' # Starting game state

game = inp.split()

# PLayer positions
positions = game[0].split("/")

player1_pos = positions[0]
player2_pos = positions[1]

# Current board fences
if (game[1] == "None"):
    curr_fences = []
else:
    curr_fences = game[1].split("/")

# Player to make move
side_to_play = int(game[2])

# Player fences reamining
fences_remaining = game[3].split("/")

player1_fen_rem = int(fences_remaining[0])
player2_fen_rem = int(fences_remaining[1])

# Board -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> 

board = Board(side_to_play, player1_pos, player1_fen_rem, player2_pos, player2_fen_rem)
board.b = fence_addition(board.b, curr_fences)

# GAME MANAGER SIMULATION -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> 

p = True

fileMinmax = open('minmax.txt', 'w')
fileMCTS = open('mcts.txt', 'w')

fileResults = open('results.txt', 'w')

while gameOver(board) == False:  # WHILE GAME IS NOT DONE
    # FIND WHICH AGENT NEEDS TO MAKE A MOVE
    if p == True:
        print("GM -> MCTS: ", inp)  # GAME STATE SENT TO MCTS
        fileResults.write(f"GM -> MCTS: {inp}\n")
        script_path = 'MCTS.py'
    else:
        print("GM -> MinMax: ", inp)  # GAME STATE SENT TO MIN-MAX
        fileResults.write(f"GM -> MinMax: {inp}\n")
        script_path = 'MinMax.py'

    # Run the script and communicate with its standard input
    process = subprocess.Popen(['python', script_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
    # Pass the input data to the script
    # Receives output from script
    out, errors = process.communicate(inp)

    out = out.strip()

    o = out.split()

    move = o[0]  # GETS AGENTS MOVE
    time = o[1]  # GETS TIME TAKEN TO MAKE MOVE

    print(script_path + '-> ', move)
    fileResults.write(f"{script_path} -> {move}\n")
    if p == True:
        fileMCTS.write(time + ", ")
    else:
        fileMinmax.write(time + ", ")

    board, curr_fences = make_move(move, board, curr_fences)  # UPDATES GM BOARD AND STATE

    # BUILDS NEW STRING TO SEND TO NEXT AGENT
    output = board.player1 + '/' + board.player2 + ' '

    if len(curr_fences) == 0:
        output = output + 'None '
    else:
        for f in curr_fences:
            if f != curr_fences[-1]:
                output = output + f + '/'
            else:
                output = output + f + ' '

    output = output + str(board.side_to_play) + ' '

    output = output + str(board.player1_fen_rem) + '/' + str(board.player2_fen_rem)

    inp = output # NEW STRING TO BE SENT
    p = not p # CHANGE TO NEXT AGENT


# RETURNS GAME WINNER
if (gameOver(board)==False):
    print("Continue")
elif (board.side_to_play == 2):
    print("MCTS wins")
    fileResults.write("MCTS wins")
else:
    print("MinMax wins")
    fileResults.write("MinMax wins")
