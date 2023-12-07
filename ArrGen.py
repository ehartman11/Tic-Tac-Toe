import numpy as np

winning_outcomes_base = [                # This is a list of the possible winning combinations based on
    [1, 2, 3],                           # a tic-tac-toe game board
    [4, 5, 6],                           # 1 | 2 | 3
    [7, 8, 9],                           # 4 | 5 | 6
    [1, 4, 7],                           # 7 | 8 | 9
    [2, 5, 8],
    [3, 6, 9],
    [1, 5, 9],
    [3, 5, 7]
]

indices = [                              # This list of indices is to be used to determine ALL the possible winning
    [0, 1, 2],                           # combinations based on order played
    [0, 2, 1],
    [1, 0, 2],
    [1, 2, 0],
    [2, 1, 0],
    [2, 0, 1],
]

winning_outcomes_comp = []               # Generate the complete list of winning combinations based on order played
for w in winning_outcomes_base:          # and then sort it.
    for i in indices:
        list_1 = []
        for r in range(3):
            list_1.append(w[i[r]])
        winning_outcomes_comp.append(list_1)
winning_outcomes_comp.sort()

win_arr = []                                                    # Generate a lookup table/array
for r in range(1, 10):                                  # 1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9
    win_val = []                                    # 1 | na    3     2     7     9     na    4     na    5
    for c in range(1, 10):                          # 2 | 3     na    1     na    8     na    na    5     na
        c_in_woc = False                            # 3 | 2     1     na    na    7     9     5     na    6
        for woc in winning_outcomes_comp:           # 4 | 7     na    na    na    6     5     1     na    na
            if (woc[0] == r) & (woc[1] == c):       # 5 | 9     8     7     6     na    4     3     2     1
                win_val.append(woc[2])              # 6 | na    na    9     5     4     na    na    na    3
                c_in_woc = True                     # 7 | 4     na    5     1     3     na    na    9     8
        if not c_in_woc:                            # 8 | na    5     na    na    2     na    9     na    7
            win_val.append("na")                    # 9 | 5     na    6     na    1     3     8     7     na
    win_arr.append(win_val)
                                                    # pos_1 row, pos_2 col, pos_3 val
win_arr = np.array(win_arr)                         # To be used in the AIs determination of the best possible option to play
