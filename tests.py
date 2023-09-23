import unittest

from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols*num_rows,
        )
        num_cols = 8
        num_rows = 15
        m2 = Maze(0, 0, num_rows, num_cols, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols*num_rows
        )
        
    def test_maze_cells_adjacent(self):
        num_cols = 8
        num_rows = 15
        m1 = Maze(0, 0, num_rows, num_cols, 20)
        for i in range(num_cols):
            for j in range(num_rows-1):
                cell = m1.get_cell(i, j)
                next_cell = m1.get_cell(i, j+1)
                self.assertEqual(
                    cell._lower_right.y,
                    next_cell._upper_left.y
                )
                
        for j in range(num_rows):
            for i in range(num_cols-1):
                cell = m1.get_cell(i, j)
                next_cell = m1.get_cell(i+1, j)
                self.assertEqual(
                    cell._lower_right.x,
                    next_cell._upper_left.x
                )
                
    def test_entrance_and_exit(self):
        num_cols = 10
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 20)
        self.assertFalse(m1.get_cell(0, 0)._has_top)
        self.assertFalse(m1.get_cell(num_cols-1, num_rows-1)._has_bottom)
        
        num_cols = 10
        num_rows = 1
        m2 = Maze(0, 0, num_rows, num_cols, 20)
        self.assertFalse(m2.get_cell(0, 0)._has_top)
        self.assertFalse(m2.get_cell(num_cols-1, num_rows-1)._has_bottom)

        num_cols = 1
        num_rows = 10
        m3 = Maze(0, 0, num_rows, num_cols, 20)
        self.assertFalse(m3.get_cell(0, 0)._has_top)
        self.assertFalse(m3.get_cell(num_cols-1, num_rows-1)._has_bottom)
        
    def test_reset(self):
        num_cols = 5
        num_rows = 5
        m = Maze(0, 0, num_rows, num_cols, 20)
        for cell in m._cells:
            self.assertFalse(cell._visited)

if __name__ == "__main__":
    unittest.main()