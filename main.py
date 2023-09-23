from window import *

def main():
    win = Window(800, 600)
    p1 = Point(100, 100)
    p2 = Point(550, 150)
    l = Line(p1, p2)
    win.draw_line(l, "black")
    win.wait_for_close()
    
    
    
if __name__ == "__main__":
    main()