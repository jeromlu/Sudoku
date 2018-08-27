# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 06:51:08 2018

@author: JEROMLU2
"""
import sys

from PyQt5.QtWidgets import QTableWidget, QItemDelegate, QLineEdit, QHeaderView
from PyQt5.QtWidgets import QApplication, QSpinBox, QTableWidgetItem, QStyledItemDelegate

from PyQt5.QtGui import QIntValidator, QFont, QIcon, QFontDatabase, QColor

from PyQt5.QtCore import Qt


ROW_NUM = 9
COL_NUM = 9
BOX_SIZE = 60

b = [[0,0,0, 9,0,4, 0,7,0],
     [0,4,0, 0,8,1, 0,0,5],
     [9,0,0, 0,0,0, 4,0,1],
     
     [0,0,3, 0,0,0, 0,5,7],
     [8,0,5, 0,0,0, 1,0,9],
     [1,6,0, 0,0,0, 3,0,0],
     
     [5,0,8, 0,0,0, 0,0,6],
     [7,0,0, 6,4,0, 0,3,0],
     [0,9,0, 8,0,7, 0,0,0]]

fd = QFontDatabase()
#print(fd.families())

# za zajbancijo

class SudokuWidget(QTableWidget):
    
    def __init__(self, parent = None):
        super(SudokuWidget, self).__init__(parent)
        
        self.setSortingEnabled(False)
        delegate = Delegate()
        self.setItemDelegate(delegate)
        self.setRowCount(ROW_NUM)
        self.setColumnCount(COL_NUM)
        self.make_square()
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        fnt = QFont()
        fnt.setPointSize(30);
        fnt.setFamily("Arial");
        
        style_sheet = '''
            QTableWidget { 
            font-size: 16pt;
            font-family: Arial Black;
            }
            QTableView::item{
            border-left: 2px solid white; 
            border-top: 2px solid white;
            }
            
        '''
        self.setStyleSheet(style_sheet)

    def make_square(self):
        
        rows = self.rowCount()
        columns = self.columnCount()
        if rows > 0:
            for row in range(rows):
                self.setRowHeight(row, BOX_SIZE)
        if columns > 0:
            for column in range(columns):
                self.setColumnWidth(column, BOX_SIZE)
                
    def populate_sudoku(self, table, color = Qt.black, table_init = None):
        '''
        populates SudokuWidget from the 2D table
        color is Qt.Color instance e.g. Qt.Green or setForeground(QColor::fromRgb(255,0,0))
        '''
        for u in range(9):
            for v in range(9):
                if (table_init is not None) and (table[u][v] - table_init[u][v]) == 0:
                    item = self.item(u, v)
                    if item is None:
                        item = QTableWidgetItem()
                        self.setItem(u, v, item)                        
                    else:
                        element = item.text()
                        item = QTableWidgetItem(element)
                        self.setItem(u, v, item)
                else:
                    element = table[u][v]
                    if element == 0:
                        item = QTableWidgetItem('')
                        self.setItem(u, v, item)
                    else:
                        item = QTableWidgetItem(str(element))
                        item.setForeground(color)
                        self.setItem(u, v, item)

                
                if self.in_quadrant(u,v) % 2 == 0:
                    item.setBackground(QColor.fromRgb(245, 245, 245))
                    
    def in_quadrant(self, row_idx, column_idx):
        '''Returns the quadrant index, see below:
         -----------
        | 0 | 1 | 2 |
         -----------
        | 3 | 4 | 5 |
         -----------
        | 6 | 7 | 8 |
        '''
        quadrant = (row_idx // 3) * 3 + (column_idx // 3)
        return quadrant


    def get_sudoku(self):
        
        sudoku = []
        print('get sudoku')
        for u in range(9):
            row = []
            for v in range(9):
                item = self.item(u, v)
                if (item is not None) and (item.text() != ''):
                    row.append(int(item.text()))
                else:
                    row.append(0)
            sudoku.append(row)
            print(row,'\n')
        return sudoku

    def clear_sudoku(self):
        
        for u in range(9):
            for v in range(9):
                item = QTableWidgetItem('')
                self.setItem(u, v, item)
                if self.in_quadrant(u,v) % 2 == 0:
                    item.setBackground(QColor.fromRgb(245, 245, 245))

                
class Delegate(QItemDelegate):
    
    def __init__(self, parent = None):
        super(Delegate, self).__init__(parent)
        
    def createEditor(self, parent, style_option, model_index):
        
        line_edit = QLineEdit(parent)
        
        int_validator = QIntValidator(1, 9, line_edit)
        line_edit.setValidator(int_validator)
        
        return line_edit
        
    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignCenter
        QItemDelegate.paint(self, painter, option, index)
        
        
    
if __name__ == '__main__':
    
    app = QApplication.instance()
    
    if app is None:
        app = QApplication(sys.argv)
        
    else:
        print('QApplication instance already exists: %s' % str(app))
    
    
    form = SudokuWidget()
    form.populate_sudoku(b, Qt.black)
    form.get_sudoku()
    form.resize(9*BOX_SIZE+7, 9*BOX_SIZE+7)
    app.setWindowIcon(QIcon("./icons/sudoku-solver-250.png"))
    form.show()
    app.exec_()
    