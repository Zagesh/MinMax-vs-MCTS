# MinMax-vs-MCTS
MinMax algorithm versus MCTS algorithm using a game manager

Game Board represented by:

<player1_postion/player2_postion\> <fence_positions> <player to move\> <fences_remaining1/fences_remaining2\>

Examples:

E1/E9 None 1 10/10

E1/E9 E3h/G6v/D8v 1 8/9

E2/F2 G6v 2 9/10

C2/C3 G6v 1 10/9

C3/C4 A2h/A3v/D1h/D2v/D3h/B4v/C4h 1 6/7

E8/A3 A2h/C2h/E2h/G2h/H2v 1 10/5

E8/A3 A2h/C2h/E2h/G2h/H2v 2 10/5

E1/B2 E3h/G6v/D8v 1 8/9

E1/E9 E3h/G6v/D8v 1 0/9

C2/E5 E7h/C7h/A7h/F8h/C6v/C4v/C2v 1 10/3

D2/D3 E7h/C7h/A7h/F8h/C6v/C4v/C2v 1 10/3

F5/E6 D8h/E7v/C7v/C5v/F7h/H7h/E5v/D1v 2 10/2

B4/D4 D8h/E7v/C7v/C5v/F7h/H7h/E5v/D1v/D2h/D5h/F2h/B5h/A4v/H2h/B2h/A1h 1 5/0

B4/D4 D8h/E7v/C7v/C5v/F7h/H7h/E5v/D1v/D2h/D5h/F2h/B5h/A4v/H2h/B2h/A1h 1 5/0

B4/G4 D8h/E7v/C7v/C5v/F7h/H7h/E5v/D1v/D2h/D5h/F2h/B5h/A4v 1 8/0
