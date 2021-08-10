import utils
import numpy as np
import time

if __name__ == "__main__":
    """---------------------------------------SETUP----------------------------------------------------"""
    flag_input = 0
    print("Enter the number of queens from number 4")
    while not flag_input:
        N = int(input())  # scelta da parte dell'utente sulla dimensione della board
        if N > 3:
            flag_input=1
            print("The dimension of the board is selected!!! GOOD!")
        else:
            print("Error insert number. Choose another number greater or equal to 4 ")

    """scelta della cella iniziale partiamo dalla riga e colonna più a sinistra"""
    row_init = 0
    col_init = 0
    count_row_index = 0  # contatore delle righe per cambiare se non va bene il posizionamento
    count_col_index = 0  # contatore delle righe per cambiare se non va bene il posizionamento
    row_index_vector = []
    # chessboard
    # NxN matrix with all elements 0
    board = [[0] * N for _ in range(N)]
    # definition of number node
    count_node = 0  # root node
    flag = 0
    row_index_old = []
    col_index = []
    row = row_init
    col = col_init
    board[row][col] = 1
    count_node += 1  # dopo aver assegnato la queen ho un nuovo nodo nel tree
    idx_refresh = 0
    list_boards = []
    row_index = []
    list_row_index = []
    list_col_index = []
    list_index_free_cells = []

    """--------------------------------------------INIT_MAIN-------------------------------------------------"""

    start = time.time()  # start computing time
    
    while not flag:

        row_index_old = row_index


        row_index, index_free_cells, board = utils.mrv(board=board, row=row, col=col, N=N)  # restituisce le righe con
                                                                                     # il minor numero di celle
                                                                                     # disponibili e le loro
                                                                                    #posizioni e la board aggiornata
        list_boards.append(np.array(board))
        list_row_index.append(row_index)
        list_index_free_cells.append(index_free_cells)
        if len(row_index) == 0:
            if np.count_nonzero(np.array(board) == 1) == N:  # abbiamo la soluzione
                end = time.time()  # end computing time
                board = np.array(board)
                board[board == 2]=0
                print("abbiamo la soluzione GOOD!\n")  # finite le celle disponibili stampa la board
                print(f"start: {start}\nend:{end}\n Runtime of the program is {end - start}\n")
                print("number of nodes is: ", count_node+1)
                count_node = 0
                time.sleep(1)

                utils.plot(N, board)
                flag = 1
            else:  # se non c'è soluzione con quella riga, cambio row index
                list_boards = list_boards[0:-1]  # tolgo l'ultimo elemento che è la ultima configurazione
                list_row_index = list_row_index[0:-1]
                list_index_free_cells = list_index_free_cells[0:-1]
                row_index = list_row_index[len(list_row_index)-1]
                index_free_cells=list_index_free_cells[len(list_index_free_cells)-1]
                board = list_boards[len(list_boards)-1]

                if count_row_index == len([row_index]):  # LASCIO QUI PER SICUREZZA count_col_index == len([col_index]) and
                    count_row_index = 0
                    list_boards = list_boards[0:-1]  # tolgo l'ultimo elemento che è la ultima configurazione
                    list_row_index = list_row_index[0:-1]
                    list_index_free_cells = list_index_free_cells[0:-1]
                    row_index = list_row_index[len(list_row_index) - 1]
                    index_free_cells = list_index_free_cells[len(list_index_free_cells) - 1]
                    board = list_boards[len(list_boards) - 1]

                if len([col_index]) > 1:  # ho ancora colonne disponibili?
                    if count_col_index <= len(col_index):
                        count_col_index += 1  # scorro l'indice delle colonne disponibili
                        col_index = col_index[count_col_index]  # cambio colonna

                        board[row_index[count_row_index]][col_index] = 1  # assegno
                        count_node += 1  # dopo aver assegnato la queen ho un nuovo nodo nel tree
                        row = row_index[count_row_index]  # assegno il nuovo valore (in questo caso la riga è fissata) da utilizzare per MRV
                        col = col_index  # assegno il nuovo valore di colonna da utilizzare per MRV
                        continue

                if len(row_index) > 1 and idx_refresh <= len(list_row_index[0]):  # caso in cui non ho più colonne da scorrere, cambio riga
                    count_col_index = 0  # prendiamo la prima colonna disponibile
                    count_row_index += 1  # cambio indice di riga
                    idx_refresh += 1

                    col_index = utils.lcv(board=board,row_chosen=row_index[count_row_index],
                                          index_free_cells=index_free_cells, N=N)  # applico lcv
                    if len(col_index) > 1:
                        col_index = col_index[count_col_index]  # ho la colonna selezionata
                    else:
                        col_index = col_index[0]
                    board[row_index[count_row_index]][col_index] = 1
                    count_node += 1  # dopo aver assegnato la queen ho un nuovo nodo nel tree
                    row = row_index[count_row_index]  # assegno il nuovo valore (in questo caso la riga è fissata) da utilizzare per MRV
                    col = col_index  # assegno il nuovo valore di colonna da utilizzare per MRV
                    continue

                else:   # non c'è soluzione finale
                    if row_init < N-1:
                        row_init += 1  # cambio riga iniziale
                        row = row_init
                        col = col_init
                        board = [[0] * N for _ in range(N)]
                        board[row][col] = 1
                        count_node += 1  # dopo aver assegnato la queen ho un nuovo nodo nel tree
                        idx_refresh=0
                        continue  # riparti dallo start state of the loop con board refreshata
                    else:
                        print("ERROR not GOOD")
                        break
        else:
            if len(row_index) > 1:
                row_index = utils.degree_heuristic(board=board, min_row_index=row_index,
                                                    index_free_cells=index_free_cells, N=N)  # restituisce il vettore di righe calcolato col degree

                if len(row_index) > 1:
                    row_index = row_index[count_row_index]  # ho la riga selezionata

            col_index = utils.lcv(board=board,row_chosen=row_index,index_free_cells=index_free_cells,N=N)

            if len(col_index) > 1:
                col_index = col_index[count_col_index]  # ho la colonna selezionata

            if type(col_index) == list:
                col_index=col_index[0]

            if type(row_index) == list:
                row_index=row_index[0]

            board[row_index][col_index] = 1
            count_node += 1  # dopo aver assegnato la queen ho un nuovo nodo nel tree
            row = row_index  # assegno il nuovo valore (in questo caso la riga è fissata) da utilizzare per MRV
            col = col_index  # assegno il nuovo valore di colonna da utilizzare per MRV


