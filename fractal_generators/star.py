from turtle import *

import turtle
tur = turtle.Turtle()
  
tur.hideturtle()
tur.speed(0)
  
tur.getscreen().bgcolor("black")
tur.color("cyan")

tur.penup()
  
tur.goto((-200, 50))
  

tur.pendown()
  

def star(turtle, size):
    if size <= 10:
        return
    else:
        for i in range(5):
            turtle.forward(size/2)
            star(turtle, size/3)
  

            # turtle.left(216)
            turtle.left(144)
  
 
# star(tur, 120)
# turtle.done()


for i in range(1, 16):
    print(i, i //2)
    if (i %2 == 0):
        size = 120 * (i // 2)
        print(size, size % 240 != 0)
        if (size % 240 != 0):
            star(tur, 120 * (i //2))

print("done")
from datetime import datetime

now = datetime.now()
turtle.getcanvas().postscript(file=f"{now}-star.eps")
# turtle.done()