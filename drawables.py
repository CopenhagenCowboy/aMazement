from tkinter import Canvas, BOTH

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Line:
    def __init__(self, p1, p2):
        self.begin = p1
        self.end = p2
        
    def draw(self, canvas, fill_color):
        canvas.create_line(self.begin.x, self.begin.y, self.end.x, self.end.y, fill=fill_color, width=2)
        canvas.pack(fill=BOTH, expand=1)
        
def get_midpoint(p1, p2):
    out = Point((p1.x + p2.x)/2., (p1.y + p2.y)/2.)
    return out
        
class Cell:
    def __init__(self, 
                 window, 
                 upper_left, 
                 lower_right, 
                 has_left_wall=True, 
                 has_right_wall=True, 
                 has_top_wall=True, 
                 has_bottom_wall=True):
        self._win = window
        self._upper_left = upper_left
        self._lower_right = lower_right
        self._has_left, self._has_right, self._has_top, self._has_bottom \
            = (has_left_wall, has_right_wall, has_top_wall, has_bottom_wall)
    
    def draw(self):
        if self._win is None:
            return
        wall = Line(self._upper_left, Point(self._upper_left.x, self._lower_right.y))
        self._win.draw_line(wall, "black" if self._has_left else "white")

        wall = Line(Point(self._lower_right.x, self._upper_left.y), self._lower_right)
        self._win.draw_line(wall, "black" if self._has_right else "white")

        wall = Line(self._upper_left, Point(self._lower_right.x, self._upper_left.y))
        self._win.draw_line(wall, "black" if self._has_top else "white")

        wall = Line(Point(self._upper_left.x, self._lower_right.y), self._lower_right)
        self._win.draw_line(wall, "black" if self._has_bottom else "white")
        # if self._has_left:
        #     wall = Line(self._upper_left, Point(self._upper_left.x, self._lower_right.y))
        #     self._win.draw_line(wall, "black")
        # if self._has_right:
        #     wall = Line(Point(self._lower_right.x, self._upper_left.y), self._lower_right)
        #     self._win.draw_line(wall, "black")
        # if self._has_top:
        #     wall = Line(self._upper_left, Point(self._lower_right.x, self._upper_left.y))
        #     self._win.draw_line(wall, "black")
        # if self._has_bottom:
        #     wall = Line(Point(self._upper_left.x, self._lower_right.y), self._lower_right)
        #     self._win.draw_line(wall, "black")
    
    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        midpoint = get_midpoint(self._upper_left, self._lower_right)
        to_midpoint = get_midpoint(to_cell._upper_left, to_cell._lower_right)
        trace = Line(midpoint, to_midpoint)
        color = "gray" if undo else "red"
        self._win.draw_line(trace, color)