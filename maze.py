from drawables import *
import time

class Maze:
    def __init__(self,
                 x,
                 y,
                 num_rows,
                 num_cols,
                 cell_size,
                 win=None
                 ):
        self._x = x
        self._y = y
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size = cell_size
        self._win = win
        self._cells = []
        
        self.create_cells()
        self.break_entrance_and_exit()
    
    def create_cells(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                upper_left = Point(self._x + i*self._cell_size, self._y + j*self._cell_size)
                lower_right = Point(self._x + (i+1)*self._cell_size, self._y + (j+1)*self._cell_size)
                cell = Cell(self._win,
                            upper_left,
                            lower_right,
                            self._cell_size)
                self._cells.append(cell)
                self.draw_cell(i, j)
    
    def get_cell(self, i, j):
        return self._cells[i*(self._num_rows) + j]
    
    def draw_cell(self, i, j):
        if self._win is None:
            return
        cell = self.get_cell(i, j)
        cell.draw()
        self.animate()
        
    def animate(self):
        self._win.redraw()
        time.sleep(0.05)
        
    def break_entrance_and_exit(self):
        self.get_cell(0, 0)._has_top = False
        self.draw_cell(0, 0)
        self.get_cell(self._num_cols-1, self._num_rows-1)._has_bottom = False
        self.draw_cell(self._num_cols-1, self._num_rows-1)