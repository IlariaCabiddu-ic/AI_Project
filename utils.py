import numpy as np
from itertools import chain
import itertools



'''--------------------------------------------MINIMUM REMAINING VALUE!---------------------------------------'''

def mrv(upload_board):

    min_row_index = []
    v_nonzero = []
    counter, index_free_cells, board = free_cells(upload_board)  # number of available values
                                                                 # available values and board
    for i in range(len(counter)):
        if counter[i] == 0:
            continue
        else:
            v_nonzero.append(counter[i])  # counter without the zeros: rows with zero available values are not needed


    if len(v_nonzero) !=0:
        Mini = np.min(v_nonzero)  # computing of the lower value of available cells
        for c in range(len(counter)):
            if counter[c] == Mini:  # check to see if there is a tie among different rows
                min_row_index.append(c)

    return min_row_index, index_free_cells, board  #  returns the rows with the lower number of values available
                                                   # the position of the free cells and board

def constraints(board, row, col, N):

    board = np.array(board)
    lim_row = max((row - col, 0))
    lim_col = max((col - row, 0))

    for i in range(N):
        board[row][i] = 2  # constraints imposed on the columns
        board[i][col] = 2  # constraints imposed on the rows

    for j in range(min((len(board), len(board[0]))) - max((lim_row, lim_col))):  # constraints imposed on the diagonal
        board[lim_row + j][lim_col + j] = 2                                      # from top left to bottom right

    board2 = np.fliplr(board)
    col1 = len(board2) - col - 1
    lim_row = max((row - col1, 0))
    lim_col = max((col1 - row, 0))
    for k in range(min((len(board2), len(board2[0]))) - max((lim_row, lim_col))):  # constraints imposed on the diagonal
        board2[lim_row + k][lim_col + k] = 2                                       # from top right to bottom left

    board = np.fliplr(board2)
    board[row][col] = 1
    board = np.array(board).tolist()

    return board  # upload board for the constraints for a given placement of the queen

def free_cells(upload_board):
    counter = []
    index_free_cells = []
    for x in upload_board:
        L = x.count(0)  # counter of the number of available values for each row
        counter.append(L)
    for r in range(len(upload_board)):
        for c in range(len(upload_board)):
            if upload_board[r][c] == 0:
                index_free_cells.append([r, c])  # list with the position f the available cells

    return counter,index_free_cells, upload_board  # returns the number of available cells per row, their position and
                                                   # the board



'''-------------------------------------------DEGREE HEURISTIC--------------------------------------------------'''


def degree_heuristic(board, min_row_index, index_free_cells, N):

    rows_index = nconflicts(board,min_row_index, index_free_cells, N)  # number of constraints imposed by each row given
                                                                       # in output from the MRV

    return rows_index  # rows involved in the max number of constraints


def nconflicts(board, min_row_index, index_free_cells, N):

    # needed to keep only the position of the free cells of the rows obtained from the MRV
    index_free_cells = np.array(index_free_cells)
    new_free_cells = []
    degree_vector_constraint = []
    loc = []
    count_degree_vector = []
    indexing = []
    degree_row = []
    sublist_degree_constraint=[]
    min_row_index = np.array(min_row_index)
    for f in min_row_index:
        a = index_free_cells[index_free_cells[:, 0] == f, :].tolist()
        new_free_cells.append(a)  # free cells only of the selected rows (from MRV)
    new_free_cells = list(itertools.chain(*new_free_cells))

    row_cells = list(item[0] for item in new_free_cells)
    col_cells = list(item[1] for item in new_free_cells)

    for g in range(len(row_cells)):
        degree_constraints = blocked_cells(board, row_cells[g], col_cells[g], N)
        degree_vector_constraint.append(degree_constraints)  # list of all the constraint imposed

    n_row_vector = np.array(row_cells)
    n_row_vector_unique = np.unique(n_row_vector)
    for i in n_row_vector_unique:
        locations = np.where(i == n_row_vector)[0]
        locations_list = locations.tolist()
        loc.append(locations_list)

    for l in loc:
        for num in l:
            sublist_degree_constraint.append(degree_vector_constraint[num])
        unnested_list = list(chain(*sublist_degree_constraint))
        unnested_list.sort()
        my_list = list(unnested_list for unnested_list, _ in itertools.groupby(unnested_list)) # delete possible doubles
        sublist_degree_constraint = []
        count_degree_vector.append([len(my_list)])  # list of all the constraint imposed by each row

    max_count = max(count_degree_vector)  # computing max values of imposed constraints
    for ind in range(len(count_degree_vector)):
        if count_degree_vector[ind] == max_count:
            indexing.append(ind)  # index of the row which imposes more constraints

    for r in indexing:
        degree_row.append(n_row_vector_unique[r])  # list of possible variables obtained applying DH

    return degree_row

def blocked_cells(board, row, col, N):  # function which counts the constraints imposed by the positioning of a queen

    list_index_cell_blocked = []
    for j in range(N):  # check the row
        if board[row][j] == 0 and j != col:  # free cell, it would get blocked if we put a queen in board[row][col]
            list_index_cell_blocked.append([row, j])
    for k in range(N):  # check the column
        if board[k][col] == 0 and k != row:  # free cell, it would get blocked if we put a queen in board[row][col]
            list_index_cell_blocked.append([k, col])

    board = np.array(board)
    lim_row = max((row - col, 0))
    lim_col = max((col - row, 0))
    # check diagonals
    for i in range(min((len(board), len(board[0]))) - max((lim_row, lim_col))):
        if board[lim_row + i][lim_col + i] == 0 and lim_row +i != row and lim_col + i != col: # free cell, it would get blocked if we put a queen in board[row][col]
            list_index_cell_blocked.append([lim_row + i,lim_col + i])

    board2 = np.fliplr(board)
    col1 = len(board2) - col - 1
    lim_row = max((row - col1, 0))
    lim_col = max((col1 - row, 0))
    for i in range(min((len(board2), len(board2[0]))) - max((lim_row, lim_col))):
        if board2[lim_row + i][lim_col + i] == 0 and lim_row + i != row and lim_col + i != col1: # free cell, it would get blocked if we put a queen in board[row][col]
            list_index_cell_blocked.append([lim_row + i, len(board2) - (lim_col + i) - 1])

    board = np.fliplr(board2)
    board[row][col] = 0
    board = np.array(board).tolist()

    return list_index_cell_blocked  # list of blocked cells


'''------------------------------------------LEAST COSTRAINING VALUE---------------------------------------------'''

def lcv(board,row_chosen, index_free_cells,N):  # row chosen from MRV or DH

    index_free_cells = np.array(index_free_cells)
    lcv_free_cells = index_free_cells[index_free_cells[:, 0] == row_chosen, :].tolist()  # only cells from selected row
    pos_queen = n_conflict_lcv(board,lcv_free_cells,row_chosen,N)

    return pos_queen


def n_conflict_lcv(board,lcv_free_cells, row_chosen,N):

    lcv_vector_constraint = []
    count_lcv_vector = []
    indexing = []
    lcv_col = []

    col_cells = list(item[1] for item in lcv_free_cells)
    if type(row_chosen) == list:
        row_chosen=row_chosen[0]
    for g in range(len(col_cells)):
        lcv_constraints = blocked_cells(board, row_chosen, col_cells[g], N)  # check the number of constraints imposed by that cell
        lcv_vector_constraint.append(lcv_constraints)  # list with cells blocked by each column

    for l in lcv_vector_constraint:
        count_lcv_vector.append(len(l))  # number of constraints imposed by each column

    min_count = min(count_lcv_vector)  # computing of the min value of imposed constraints
    for ind in range(len(count_lcv_vector)):
        if count_lcv_vector[ind] == min_count:
            indexing.append(ind)  # check if there's a tie between columns

    for r in indexing:
        lcv_col.append(col_cells[r])  # selected value

    return lcv_col

"""-----------------------PLOTTING RESULTS--------------------------------------------------------------"""


def plot(N,board):  # Plot the solution on a chessboard
    import seaborn as sns
    import matplotlib.pyplot as plt

    plt.close('all')
    plt.figure(figsize=(10, 10))
    sns.heatmap(board, linewidths=.8, cbar=False, linecolor='blue',
                cmap='Reds', center=0.4)

    csfont = {'fontname': 'Times New Roman'}
    plt.title(f"This is a solution of {N} queens\n", fontsize= 30, **csfont)

    plt.show()
