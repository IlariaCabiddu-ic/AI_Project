import numpy as np
from itertools import chain
import itertools



'''--------------------------------------------MINIMUM REMAINING VALUE!---------------------------------------'''

def mrv(upload_board):

    min_row_index = []
    v_nonzero = []
    counter, index_free_cells, board = free_cells(upload_board)  # numero di celle libere
                                                                       # con le loro posizioni e la board aggiornata
    for i in range(len(counter)): # scorro su tutto il vettore dei conteggi delle celle libere
        if counter[i] == 0:
            continue
        else:
            v_nonzero.append(counter[i]) # prendo i valori non nulli dal vettore counter perchè devo prendere il
                                         # minimo ma non il nullo

    if len(v_nonzero) !=0:
        Mini = np.min(v_nonzero)  # calcolo il minimo numero delle celle libere
        for c in range(len(counter)):
            if counter[c] == Mini:  # confronto il minimo con le altre righe
                min_row_index.append(c)  # se ci sono più minimi uguali voglio tracciare entrambi

    return min_row_index, index_free_cells, board  # restituisce le righe con il minor numero di celle disponibili
                                            # e le loro posizioni e la board aggiornata

def constraints(board, row, col, N):  # da definire
    """cella libera :0
       cella occupata da una regina : 1
       cella bloccata da una regina : 2 """
    board = np.array(board)
    lim_row = max((row - col, 0))
    lim_col = max((col - row, 0))

    for i in range(N):
        board[row][i] = 2
        board[i][col] = 2

    for j in range(min((len(board), len(board[0]))) - max((lim_row, lim_col))): # blocco le diagonali
        board[lim_row + j][lim_col + j] = 2

    board2 = np.fliplr(board)
    col1 = len(board2) - col - 1
    lim_row = max((row - col1, 0))  # 2
    lim_col = max((col1 - row, 0))  # 0
    for k in range(min((len(board2), len(board2[0]))) - max((lim_row, lim_col))):
        board2[lim_row + k][lim_col + k] = 2

    board = np.fliplr(board2)
    board[row][col] = 1
    board = np.array(board).tolist()

    return board  # restituisce la board aggiornata

def free_cells(upload_board):
    counter = []
    index_free_cells = []
    for x in upload_board:
        L = x.count(0) # conteggio del numero di celle libere su ogni riga
        counter.append(L) # inserisci su un vettore tutti i conteggi
    for r in range(len(upload_board)):
        for c in range(len(upload_board)):
            if upload_board[r][c] == 0:
                index_free_cells.append([r, c])

    return counter,index_free_cells, upload_board # numero di celle libere su ogni riga e le loro posizioni e la board aggiornata



'''-------------------------------------------DEGREE HEURISTIC--------------------------------------------------'''


def degree_heuristic(board, min_row_index, index_free_cells, N): # board, righe con minimo numero di celle libere,
                                                                # posizione delle celle libere, dimensione board

    rows_index = nconflicts(board,min_row_index, index_free_cells, N) # restituisce il numero di costraints che impone
                                                                   # ogni riga scelta dalla mrv (min_index)

    return rows_index  # restituisce il vettore di righe che impongono più costraint agli altri


def nconflicts(board, min_row_index, index_free_cells, N):  # board, righe con minimo numero di celle libere,
                                                          # posizione delle celle libere, dimensione board
    # tengo solo gli indici delle celle delle righe che ci interessano (quelle con il minor numero di celle libere)
    index_free_cells = np.array(index_free_cells) # converto in array per ottenere dalla prima colonna (dove viene
                                                  # indicata la riga) solo le celle della riga scelta da min_row_index
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
        new_free_cells.append(a) # nuova lista delle celle libere con solo le righe di interesse (quello che ci dà mrv)
    new_free_cells = list(itertools.chain(*new_free_cells))
    ''' modifica la board provando a posizionare una regina (concettualmente), devo contare le nuove celle che cambio'''
    row_cells = list(item[0] for item in new_free_cells)  # slicing delle sole righe
    col_cells = list(item[1] for item in new_free_cells)  # slicing delle sole righe
    for g in range(len(row_cells)):  # faccio un unico for perchè n righe ed n colonne sono uguali
        # print("row_cell_g" , row_cells)
        degree_constraints = blocked_cells(board, row_cells[g], col_cells[g], N)
        degree_vector_constraint.append(degree_constraints)  # listona con tutte le celle bloccate relativa ad ogni riga

    n_row_vector = np.array(row_cells)
    n_row_vector_unique = np.unique(n_row_vector)
    for i in n_row_vector_unique:  # cerco gli indici degli elementi duplicati in modo da poter togliere i doppioni
        locations = np.where(i == n_row_vector)[0]
        locations_list = locations.tolist()
        loc.append(locations_list)  # indici delle celle delle stesse righe

    for l in loc:
        for num in l:
            sublist_degree_constraint.append(degree_vector_constraint[num])
        unnested_list = list(chain(*sublist_degree_constraint))
        unnested_list.sort()
        my_list = list(unnested_list for unnested_list, _ in itertools.groupby(unnested_list)) # listona di tutte le celle bloccate da ogni relativa togliendo i doppioni
        sublist_degree_constraint = []
        count_degree_vector.append([len(my_list)])  # calcolo del numero di celle bloccate da ogni riga

    max_count = max(count_degree_vector) # calcolo del massimo numero di celle bloccate
    for ind in range(len(count_degree_vector)):
        if count_degree_vector[ind] == max_count:
            indexing.append(ind)  # in questo modo ho l'indice delle righe che blocca più celle

    for r in indexing: # devo prenderli da row_vector_unique perchè così sono certa quali siano le righe
        degree_row.append(n_row_vector_unique[r])  # restituisce le righe calcolate dal degree heuristic

    return degree_row # restituisce le righe che bloccano il numero più alto di celle

def blocked_cells(board, row, col, N):

    list_index_cell_blocked = []
    for j in range(N):  # controlla tutta la riga
        if board[row][j] == 0 and j != col:  # cella libera, va in list_cell_blocked nel caso in cui posizionassi una regina in board[row][col]
            list_index_cell_blocked.append([row, j])
    for k in range(N):  # controllo tutta la colonna
        if board[k][col] == 0 and k != row:  # cella libera, va in list_cell_blocked nel caso in cui posizionassi una regina in board[row][col]
            list_index_cell_blocked.append([k, col])

    board = np.array(board)
    lim_row = max((row - col, 0))
    lim_col = max((col - row, 0))
    for i in range(min((len(board), len(board[0]))) - max((lim_row, lim_col))):
        if board[lim_row + i][lim_col + i] == 0 and lim_row +i != row and lim_col + i != col:
            list_index_cell_blocked.append([lim_row + i,lim_col + i])

    board2 = np.fliplr(board)
    col1 = len(board2) - col - 1
    lim_row = max((row - col1, 0))
    lim_col = max((col1 - row, 0))
    for i in range(min((len(board2), len(board2[0]))) - max((lim_row, lim_col))):
        if board2[lim_row + i][lim_col + i] == 0 and lim_row + i != row and lim_col + i != col1:
            list_index_cell_blocked.append([lim_row + i, len(board2) - (lim_col + i) - 1])

    board = np.fliplr(board2)
    board[row][col] = 0  # ripristino il valore a quello di prima
    board = np.array(board).tolist()

    return list_index_cell_blocked  # restituisce la lista di tutte le celle bloccate


'''------------------------------------------LEAST COSTRAINING VALUE---------------------------------------------'''

def lcv(board,row_chosen, index_free_cells,N): # row_choised: riga che sarà scelta o dal mrv o da degree

    index_free_cells = np.array(index_free_cells)
    lcv_free_cells = index_free_cells[index_free_cells[:, 0] == row_chosen, :].tolist() # prendo tutte le celle con la riga selezionata dal degree heuritic
    pos_queen = n_conflict_lcv(board,lcv_free_cells,row_chosen,N)

    return pos_queen


def n_conflict_lcv(board,lcv_free_cells, row_chosen,N):

    lcv_vector_constraint = []
    count_lcv_vector = []
    indexing = []
    lcv_col = []
    ''' modifica la board provando a posizionare una regina (concettualmente), devo contare le nuove celle che cambio'''
    col_cells = list(item[1] for item in lcv_free_cells)  # slicing delle colonne celle libere
    if type(row_chosen) == list:
        row_chosen=row_chosen[0]
    for g in range(len(col_cells)):
        lcv_constraints = blocked_cells(board, row_chosen, col_cells[g], N)  #richiamo blocked cells per vedere quante celle blocca
        lcv_vector_constraint.append(lcv_constraints)  # listona con tutte le celle bloccate relativa ad ogni colonna

    for l in lcv_vector_constraint:
        count_lcv_vector.append(len(l)) # conteggio delle celle bloccate relativa ad ogni colonna della riga selezionata

    min_count = min(count_lcv_vector) # calcolo il minimo numero di celle bloccate
    for ind in range(len(count_lcv_vector)):
        if count_lcv_vector[ind] == min_count:
            indexing.append(ind)  # in questo modo ho l'indice delle righe che blocca più celle

    for r in indexing:  # devo prenderli da row_vector_unique perchè così sono certa quali siano le righe
        lcv_col.append(col_cells[r])  # restituisce le colonne calcolate dal lcv

    return lcv_col  #  possibile colonna da selezionare perchè la riga è già stata scelta

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
