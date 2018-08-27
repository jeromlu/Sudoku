# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 21:48:03 2018

@author: JEROMLU2
"""

import sys
import os
import copy


from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QMessageBox
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QHBoxLayout

from PyQt5.QtGui import QIcon

from PyQt5.QtCore import Qt

import sudoku_widget_class

b = [[0,0,0, 9,0,4, 0,7,0],
     [0,4,0, 0,8,1, 0,0,5],
     [9,0,0, 0,0,0, 4,0,1],
     
     [0,0,3, 0,0,0, 0,5,7],
     [8,0,5, 0,0,0, 1,0,9],
     [1,6,0, 0,0,0, 3,0,0],
     
     [5,0,8, 0,0,0, 0,0,6],
     [7,0,0, 6,4,0, 0,3,0],
     [0,9,0, 8,0,7, 0,0,0]]

c = [[5,0,0, 0,0,0, 0,3,2],
     [0,7,0, 0,0,1, 0,4,0],
     [0,9,0, 4,2,0, 0,0,7],
     
     [0,0,9, 0,0,2, 0,6,0],
     [0,0,2, 6,1,8, 7,0,0],
     [0,6,0, 7,0,0, 2,0,0],
     
     [8,0,0, 0,7,3, 0,5,0],
     [0,1,0, 2,0,0, 0,7,0],
     [9,3,0, 0,0,0, 0,0,6]]


class MainWindow(QMainWindow):
    
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        
        #data
        self.sudoku_init = None
        self.sudoku_solved = None
        self.solved = False
        

        #UI
        self.setup_UI()
        
        #testni sudoku
        self.sudoku_widget.populate_sudoku(c, Qt.black)

        
        #connections
        self.btn_solve.clicked.connect(self.find_solution)
        self.btn_clear.clicked.connect(self.clear_sudoku)
        
        
    def setup_UI(self):
        
        
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        self.sudoku_widget = sudoku_widget_class.SudokuWidget(self.main_widget)
        
        #label_sudoku = QLabel('Sudoku: ')
        self.btn_solve = QPushButton('Solve')
        self.btn_clear = QPushButton('Clear')
        
        solve_hbox = QHBoxLayout()
        solve_hbox.addWidget(self.btn_solve)
        solve_hbox.addWidget(self.btn_clear)
        solve_hbox.addStretch(1)
        
        
        
        main_layout = QVBoxLayout(self.main_widget)
        #main_layout.addWidget(label_sudoku)
        main_layout.addWidget(self.sudoku_widget)
        main_layout.addLayout(solve_hbox)

        
        #self.setCentralWidget(sudoku_widget)
        self.setLayout(main_layout)
        
    def clear_sudoku(self):
        self.sudoku_widget.clear_sudoku()
        self.sudoku_init = None
        self.solved = False
        
    def find_solution(self):
        
        try:
            self.sudoku_init = self.sudoku_widget.get_sudoku()
            self.izpis(self.sudoku_init)
            self.sudoku_solved = copy.deepcopy(self.sudoku_init)
            self.izpis(self.sudoku_solved)
            print('\n')
            print(self.sudoku_solved is self.sudoku_init)
            self.izpis(self.sudoku_init)
            self.backtrack(0,0)
            self.solved = True
            print('\n\n')
            self.izpis(self.sudoku_init)
            print('\n')
            print(self.sudoku_solved is self.sudoku_init)
            self.izpis(self.sudoku_solved)
            
            self.sudoku_widget.populate_sudoku(self.sudoku_solved, Qt.green, self.sudoku_init)
            
            
        except:
            self.print_err()
        
        
    

    def backtrack(self, u,v):
        # (u,v) je koordinata, v kateri moramo preizkusiti vse moznosti.
        # premaknemo se v naslednje prazno polje
        sudoku = self.sudoku_solved
        
        while u < 9 and sudoku[u][v] != 0: 
            (u,v) = self.next_field(u,v)
        if (u,v) == (9,0):
            # obdelali smo vsa polja in nasli resitev
            return sudoku
        else:
            # izracunamo vse dovoljene poteze za polje (u,v)
            #print(t)
            for k in self.possible_moves(u,v, sudoku):
                sudoku[u][v] = k
                r = self.backtrack(u,v)
                if r is None:
                    # odstranimo potezo
                    sudoku[u][v] = 0
                else:
                    # nasli smo resitev
                    return r
            # Pregledali smo vse poteze, ni resitve
            return None

        
    def next_field(self, u,v):
        '''
        moves onto the next filed (row first)
        '''
        if v < 8:
            return (u, v+1)
        else:
            return (u+1, 0)
        
    def quadrant(self, n):
        ''' determines in which quadrant the index is
        '''
        if n < 3:
            return 3
        elif n < 6:
            return 6
        else:
            return 9

    def possible_moves(self, u,v, sudoku):
        '''
        finds all possible values that are allowed to inser into the
        field at position u, v
        '''
        #poglej vrstico
        if sudoku[u][v] != 0:
            return []
        allowed_numbers = []
        vrednosti = sudoku[u].copy()
        #dodam vrednosti v stolpcu
        for i in range(9):
            vrednosti.append(sudoku[i][v])
        #dodam se vrednosti v kvadratku
        for row in sudoku[self.quadrant(u)-3 : self.quadrant(u)]:
            for val in row[self.quadrant(v)-3 : self.quadrant(v)]:
                vrednosti.append(val)
        #vrednosti  = [y for x in vrednosti for y in x]
        for value in [1,2,3,4,5,6,7,8,9]:
            #preveri po vrstici
            if value not in vrednosti:
                allowed_numbers.append(value)
        return allowed_numbers
        
    def print_err(self):
            exc_type, exc_obj, exc_tb = sys.exc_info()           
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err_msg = '{0}:\n{1}\nError occurred in file: {2}'.format(exc_type, exc_obj, fname)
            QMessageBox.critical(self, 'Error - see below', err_msg)
            
    def izpis(self, table):
        for i in range(9):
            print(table[i])
        
if __name__ == '__main__':
    app = QApplication.instance()    
    
    if app is None:
        app = QApplication(sys.argv)
    else:
        print('QApplication instance already exists: %s' % str(app))

    form = MainWindow()
    form.resize(9*sudoku_widget_class.BOX_SIZE+22, 9*sudoku_widget_class.BOX_SIZE+52)
    app.setWindowIcon(QIcon("./icons/sudoku-solver-250.png"))
    #app.setWindowIcon(QIcon("./icons/tv-icon.png"))
    #app.setApplicationName("RTV video downloader (samo radijske oddaje)")
    form.show()
    app.exec_()

