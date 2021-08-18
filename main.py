import utils
import numpy as np
import time

if __name__ == "__main__":
    """---------------------------------------SETUP----------------------------------------------------"""
    flag_input = 0
    print("Enter a number of queens higher than 4:")
    while not flag_input:
        N = int(input())  # N is the number of queens and dimension of the board chosen by the user
        if N > 3:
            flag_input = 1
            print("The dimension of the board is correctly selected!")
        else:
            print("Error! Choose another number greater or equal to 4 ")

    """Selection of the position of the first queen on the board: first row and first column"""
    row_init = 0
    col_init = 0
    count_row_index = 0  # counter needed in case of tie between rows
    count_col_index = 0  # counter needed in case of tie between columns
    row_index_vector = []
    # chessboard
    # NxN matrix with all elements 0
    board = [[0] * N for _ in range(N)]
    # definition of number node
    count_node = 0  # root node
    flag = 0
    col_index = []
    row = row_init
    col = col_init
    board[row][col] = 1  # positioning of the first queen, random choice without heuristics
    count_node += 1  # counter for the expanded nodes
    idx_refresh = 0
    list_boards = []
    row_index = []
    list_row_index = []
    list_col_index = []
    list_index_free_cells = []

    """--------------------------------------------INIT_MAIN-------------------------------------------------"""

    start = time.time()  # start computing time

    while not flag:

        upload_board = utils.constraints(board=board, row=row, col=col, N=N)  # board with the unavailable cells

        row_index, index_free_cells, board = utils.mrv(upload_board=upload_board)  # row with the lower number of
                                                                                   # available values

        list_boards.append(np.array(board))  # backup boards needed in case no solution is found on the first try
        list_row_index.append(row_index)
        list_index_free_cells.append(index_free_cells)
        if len(row_index) == 0:
            if np.count_nonzero(np.array(board) == 1) == N:  # solution found since N queen are placed on the board
                end = time.time()
                board = np.array(board)
                board[board == 2] = 0
                print("We have he solution!\n")
                print(f"start: {start}\nend:{end}\n Runtime of the program is {end - start}\n")
                print("number of expanded nodes is: ", count_node+1)
                count_node = 0
                time.sleep(1)

                utils.plot(N, board)
                flag = 1
            else:  # no solution found, backtracking
                list_boards = list_boards[0:-1]  # delete the previous board which led to no solution
                list_row_index = list_row_index[0:-1]
                list_index_free_cells = list_index_free_cells[0:-1]
                row_index = list_row_index[len(list_row_index)-1]
                index_free_cells=list_index_free_cells[len(list_index_free_cells)-1]
                board = list_boards[len(list_boards)-1]

                if count_row_index == len([row_index]):
                    count_row_index = 0
                    list_boards = list_boards[0:-1]
                    list_row_index = list_row_index[0:-1]
                    list_index_free_cells = list_index_free_cells[0:-1]
                    row_index = list_row_index[len(list_row_index) - 1]
                    index_free_cells = list_index_free_cells[len(list_index_free_cells) - 1]
                    board = list_boards[len(list_boards) - 1]

                if len([col_index]) > 1:  # try new values for the previously selected variable if there were more than
                                          # one in output from the LCV
                    if count_col_index <= len(col_index):
                        count_col_index += 1
                        col_index = col_index[count_col_index]  # change value

                        board[row_index[count_row_index]][col_index] = 1  # assign queen to the new position
                        count_node += 1  # count the new expanded node
                        row = row_index[count_row_index]  # selected variable
                        col = col_index  # selected value
                        continue

                if len(row_index) > 1 and idx_refresh <= len(list_row_index[0]):  # no more values available, need to
                                                                                  # change variable
                    count_col_index = 0
                    count_row_index += 1  # new variable selected
                    idx_refresh += 1

                    col_index = utils.lcv(board=board,row_chosen=row_index[count_row_index],
                                          index_free_cells=index_free_cells, N=N)  # lcv applied to the new variable
                    if len(col_index) > 1:
                        col_index = col_index[count_col_index]  # selected value
                    else:
                        col_index = col_index[0]
                    board[row_index[count_row_index]][col_index] = 1  # positioning of the queen
                    count_node += 1  # new node expanded
                    row = row_index[count_row_index]  # selected variable
                    col = col_index  # selected value
                    continue

                else:   # after backtracking up the root node, need to change position of the first queen
                    if row_init < N-1:
                        row_init += 1  # different first variable selected
                        row = row_init
                        col = col_init
                        board = [[0] * N for _ in range(N)]
                        board[row][col] = 1
                        count_node += 1  # new expanded node
                        idx_refresh=0
                        continue  # start again
                    else:
                        print("ERROR not GOOD")
                        break
        else:
            if len(row_index) > 1:
                row_index = utils.degree_heuristic(board=board, min_row_index=row_index,
                                                    index_free_cells=index_free_cells, N=N)  # tie breaker after MRV

                if len(row_index) > 1:
                    row_index = row_index[count_row_index]  # in case of tie also after DH

            col_index = utils.lcv(board=board,row_chosen=row_index,index_free_cells=index_free_cells,N=N)

            if len(col_index) > 1:
                col_index = col_index[count_col_index]  # in case of tie after LCV

            if type(col_index) == list:
                col_index = col_index[0]

            if type(row_index) == list:
                row_index = row_index[0]

            board[row_index][col_index] = 1
            count_node += 1  # positioning of the queen
            row = row_index  # selected variable
            col = col_index  # selected value
