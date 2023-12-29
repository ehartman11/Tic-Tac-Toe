import numpy as np

win_oc = [                # This is a list of the possible winning combinations based on
    [1, 2, 3],                           # a tic-tac-toe game board
    [4, 5, 6],                           # 1 | 2 | 3
    [7, 8, 9],                           # 4 | 5 | 6
    [1, 4, 7],                           # 7 | 8 | 9
    [2, 5, 8],
    [3, 6, 9],
    [1, 5, 9],
    [3, 5, 7]
]

win_ind = [                              # This list of indices is to be used to determine ALL the possible winning
    [0, 1, 2],                           # combinations based on order played
    [0, 2, 1],
    [1, 0, 2],
    [1, 2, 0],
    [2, 1, 0],
    [2, 0, 1],
]

tot_w_oc = []               # Generate the complete list of winning combinations
for wc in win_oc:          
    for wi in win_ind:
        l1 = []
        for i in wi:
            l1.append(wc[i])
        tot_w_oc.append(l1)

win_arr = np.zeros((9, 9), dtype=int)           # Generate a lookup table/array
for oc in tot_w_oc:                                      #  1 |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9
    win_arr[oc[0] - 1][oc[1] - 1] = oc[2]            # 1 | na    3     2     7     9     na    4     na    5
                                                     # 2 | 3     na    1     na    8     na    na    5     na
                                                     # 3 | 2     1     na    na    7     9     5     na    6
                                                     # 4 | 7     na    na    na    6     5     1     na    na
                                                     # 5 | 9     8     7     6     na    4     3     2     1
                                                     # 6 | na    na    9     5     4     na    na    na    3
                                                     # 7 | 4     na    5     1     3     na    na    9     8
                                                     # 8 | na    5     na    na    2     na    9     na    7
                                                     # 9 | 5     na    6     na    1     3     8     7     na

                                                    # pos_1 row, pos_2 col, pos_3 val
                                                    # To be used in the AIs determination of the best possible option to play
