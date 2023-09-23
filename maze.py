from drawables import *
import random
import time


'''
A maze consists of a grid of cells, some of whose walls are broken down
to give paths through the maze.
'''
class Maze:
    '''
    First creates an empty maze, then generates its cell grid,
    after which it breaks down walls to form paths through the maze.
    Finally solves the maze, draws the solution and stores it in _solution.
    '''
    def __init__(self,
                 x,
                 y,
                 num_rows,
                 num_cols,
                 cell_size_x,
                 cell_size_y,
                 window=None, 
                 seed=None):
        self._x = x
        self._y = y
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = window
        self._cells = []
        
        self.create_cells()
        self.break_entrance_and_exit()
        
        random.seed(seed)
        self.break_walls()
        self._solution = self.solve()
    
    
    '''
    Cells are stored in column first order in self._cells, so that
    the (i, j)th cell in the grid has index i*_num_rows + j in self._cells.
    '''
    def create_cells(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                upper_left = Point(self._x + i*self._cell_size_x, self._y + j*self._cell_size_y)
                lower_right = Point(self._x + (i+1)*self._cell_size_x, self._y + (j+1)*self._cell_size_y)
                cell = Cell(self._win,
                            upper_left,
                            lower_right)
                self._cells.append(cell)
                self.draw_cell(i, j, animate=False)
    
    def get_cell(self, i, j):
        return self._cells[i*(self._num_rows) + j]
    
    def draw_cell(self, i, j, animate = True):
        if self._win is None:
            return
        cell = self.get_cell(i, j)
        cell.draw()
        if animate:
            self.animate()
        
    def animate(self, pause_time = 0.05):
        self._win.redraw()
        time.sleep(pause_time)
    
    
    '''
    Breaks open the top resp. bottom walls at the first (top left) 
    resp. final (bottom right) cells. These are the only exterior
    cells whose outward-facing walls are broken.
    '''    
    def break_entrance_and_exit(self):
        self.get_cell(0, 0)._has_top = False
        self.draw_cell(0, 0, animate=False)
        self.get_cell(self._num_cols-1, self._num_rows-1)._has_bottom = False
        self.draw_cell(self._num_cols-1, self._num_rows-1, animate=False)
        self.animate(1)
        
        
    def get_adjacent_cells(self, i, j):
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
    
    
    '''
    Cells are considerd connected if they are adjacent and the wall between them is broken down.
    '''
    def are_connected(self, first_idc, second_idc):
        side_by_side = abs(first_idc[0]-second_idc[0]) == 1 and first_idc[1] == second_idc[1]
        over_and_under = abs(first_idc[1] - second_idc[1]) == 1 and first_idc[0] == second_idc[0]
        if not (over_and_under or side_by_side):
            return False
        
        first_cell = self.get_cell(first_idc[0], first_idc[1])
        second_cell = self.get_cell(second_idc[0], second_idc[1])
        if over_and_under:
            if first_idc[1] < second_idc[1]:
                return not first_cell._has_bottom
            else:
                return not second_cell._has_bottom
        elif side_by_side:
            if first_idc[0] < second_idc[0]:
                return not first_cell._has_right
            else:
                return not second_cell._has_right 
    
    
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
    
    
    '''
    Recursive method implementing a breadth first search through the grid to break down
    walls in order to form paths through the maze, one of which is the solution.
    There can be no loops through the maze and therfore only exactly one solution.
    '''    
    def break_walls_r(self, i, j):
        curr_cell = self.get_cell(i, j)
        curr_cell._visited = True
        adj = self.get_adjacent_cells(i, j)
        while not len(adj) == 0:
            unvisited_adj = [nb for nb in adj if not self.get_cell(nb[0], nb[1])._visited]
            if len(unvisited_adj) == 0:
                break
            idx = random.randrange(0, len(unvisited_adj))
            next_cell = unvisited_adj[idx]
            self.break_wall_between_adjacent_cells((i, j), next_cell)
            self.break_walls_r(next_cell[0], next_cell[1])
        self.draw_cell(i, j)
        
        
    def break_walls(self):
        self.break_walls_r(0, 0)
        self.reset_cells_visited()
        self.animate(1)
        
        
    def reset_cells_visited(self):
        for cell in self._cells:
            cell._visited = False
            
    '''
    Recursive method implementing a depth first search for the solution to the maze.
    Returns a list of cells indicating the path trough the maze taking you from the first
    to the final cell.
    '''        
    def solve_r(self, i, j):
        curr_cell = self.get_cell(i, j)
        curr_cell._visited = True
        if i == 0 and j== 0:
            return [(i, j)]
        unprocessed = [nb for nb in self.get_adjacent_cells(i, j) if self.are_connected((i, j), (nb[0], nb[1]))]
        while not len(unprocessed) == 0:
            next_cell = unprocessed.pop()
            if self.get_cell(next_cell[0], next_cell[1])._visited:
                continue
            sol = self.solve_r(next_cell[0], next_cell[1])
            if (len(sol) > 0):
                sol.append((i, j))
                return sol
        return []
    
    
    def solve(self):
        sol = self.solve_r(self._num_cols-1, self._num_rows-1)
        for i in range(len(sol)-1):
            curr_cell = self.get_cell(sol[i][0], sol[i][1])
            next_cell = self.get_cell(sol[i+1][0], sol[i+1][1])
            curr_cell.draw_move(next_cell)
            self.animate(0.1)
        
        return sol
            