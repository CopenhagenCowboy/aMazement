from drawables import *
import random
import time

class Maze:
    def __init__(self,
                 x,
                 y,
                 num_rows,
                 num_cols,
                 cell_size,
                 win=None, 
                 seed=None):
        self._x = x
        self._y = y
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size = cell_size
        self._win = win
        self._cells = []
        
        self.create_cells()
        self.break_entrance_and_exit()
        random.seed(seed)
        self.break_walls(0, 0)
        self.reset_cells_visited()
    
    def create_cells(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                upper_left = Point(self._x + i*self._cell_size, self._y + j*self._cell_size)
                lower_right = Point(self._x + (i+1)*self._cell_size, self._y + (j+1)*self._cell_size)
                cell = Cell(self._win,
                            upper_left,
                            lower_right)
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
        time.sleep(0.01)
        
    def break_entrance_and_exit(self):
        self.get_cell(0, 0)._has_top = False
        self.draw_cell(0, 0)
        self.get_cell(self._num_cols-1, self._num_rows-1)._has_bottom = False
        self.draw_cell(self._num_cols-1, self._num_rows-1)
        
    def get_adjacent(self, i, j):
        adj = []
        if i > 0:
            adj.append((i-1, j))
        if i < self._num_cols-1:
            adj.append((i+1, j))
        if j > 0:
            adj.append((i, j-1))
        if j < self._num_rows-1:
            adj.append((i, j+1))
            
        return adj
    
    def break_wall_between_adjacent_cells(self, first_idc, second_idc):
        side_by_side = abs(first_idc[0]-second_idc[0]) == 1 and first_idc[1] == second_idc[1]
        over_and_under = abs(first_idc[1] - second_idc[1]) == 1 and first_idc[0] == second_idc[0]
        if not (over_and_under or side_by_side):
            print("Warning: break_wall called on non-adjacent or equal cells")
            return
        
        first_cell = self.get_cell(first_idc[0], first_idc[1])
        second_cell = self.get_cell(second_idc[0], second_idc[1])
        if over_and_under:
            if (first_idc[1] < second_idc[1]):
                first_cell._has_bottom = False
                second_cell._has_top = False
            else:
                first_cell._has_top = False
                second_cell._has_bottom = False
        elif side_by_side:
            if (first_idc[0] < second_idc[0]):
                first_cell._has_right = False
                second_cell._has_left = False
            else:
                first_cell._has_left = False
                second_cell._has_right = False
        
    def break_walls(self, i, j):
        curr_cell = self.get_cell(i, j)
        curr_cell._visited = True
        adj = self.get_adjacent(i, j)
        while not len(adj) == 0:
            unvisited_adj = [nb for nb in adj if not self.get_cell(nb[0], nb[1])._visited]
            if len(unvisited_adj) == 0:
                break
            idx = random.randrange(0, len(unvisited_adj))
            next_cell = unvisited_adj[idx]
            self.break_wall_between_adjacent_cells((i, j), next_cell)
            self.break_walls(next_cell[0], next_cell[1])
        self.draw_cell(i, j)
        
    def reset_cells_visited(self):
        for cell in self._cells:
            cell._visited = False
            