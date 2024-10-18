import turtle
from math import sqrt

def draw_triangle(x1, y1, x2, y2, x3, y3, t):
    t.up()
    t.setpos(x1, y1)
    t.down()
    t.setpos(x2, y2)
    t.setpos(x3, y3)
    t.setpos(x1, y1)
    t.up()

def draw_koch(x1, y1, x2, y2, t):
    d = sqrt((x1 - x2)**2 + (y1 - y2)**2)
    r = d / 3.0
    h = sqrt(3.0) / 2.0 * r
    p1 = ((2 * x1 + x2)/ 3.0, (2 * y1 + y2)/ 3.0)
    p3 = ((2 * x2 + x1)/ 3.0, (2 * y2 + y1)/ 3.0)
    c = ((x1 + x2)/ 2.0, (y1 + y2)/ 2.0 )
    n = ((y1 - y2)/ d, (x2 - x1)/d)
    p2 = (c[0]+h*n[0], c[1]+h*n[1])

    # 绘制图形
    if d > 10:
        draw_koch(x1, y1, p1[0], p1[1], t)
        draw_koch(p1[0], p1[1], p2[0], p2[1], t)
        draw_koch(p2[0], p2[1], p3[0], p3[1], t)
        draw_koch(p3[0], p3[1], x2, y2, t)
    else:
        t.up()
        t.setpos(x1, y1)
        t.down()
        t.setpos(p1[0], p1[1])
        t.setpos(p2[0], p2[1])
        t.setpos(p3[0], p3[1])
        t.setpos(x2, y2)
        t.up()
        

def main():
    t = turtle.Turtle()
    t.hideturtle()
    draw_koch(-100, 0, 100, 0, t)
    turtle.Screen().exitonclick()

if __name__ == '__main__':
    main()
