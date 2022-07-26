import turtle

t = turtle.Turtle()
t.getscreen().bgcolor("black")
t.color("cyan")

t.hideturtle()
t.shape("turtle")
t.speed(0)

def tree(size, levels, angle):
	if levels == 0:
		# color("green")
		# dot(size)
		# color("black")
		return

	t.forward(size)
	t.right(angle)

	tree(size * 0.8, levels - 1, angle)

	t.left(angle * 2)

	tree(size * 0.8, levels - 1, angle)

	t.right(angle)
	t.backward(size)


def snowflake_side(length, levels):
	if levels == 0:
		t.forward(length)
		return

	length /= 3.0
	snowflake_side(length, levels - 1)
	t.left(60)
	snowflake_side(length, levels - 1)
	t.right(120)
	snowflake_side(length, levels - 1)
	t.left(60)
	snowflake_side(length, levels - 1)


def create_snowflake(sides, length):
	colors = ["green", "blue", "yellow", "orange", "red"]
	for i in range(sides):
		# t.color(colors[i%len(colors)])
		snowflake_side(length, sides)
		t.right(360 / sides)

####################################### SNOW FLAKE #####################################	
import random
sfcolor = ["blue", "purple", "grey", "magenta"]

def snowflake(size):
 
    # move the pen into starting position
    t.penup()
    t.forward(10*size)
    t.left(45)
    t.pendown()
    # t.color(random.choice(sfcolor))
 
    # draw branch 8 times to make a snowflake
    for i in range(8):
        branch(size)  
        t.left(45)

def branch(size):
    for i in range(3):
        for i in range(3):
            t.forward(10.0*size/3)
            t.backward(10.0*size/3)
            t.right(45)
        t.left(90)
        t.backward(10.0*size/3)
        t.left(45)
    t.right(90)
    t.forward(10.0*size)     

####################################### SNOW FLAKE #####################################

####################################### GET CIRCLE CIRUMFERENCE POINTS #####################################
import math
pi = math.pi

def PointsInCircum(r,n=100):
    return [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n+1)]

####################################### GET CIRCLE CIRUMFERENCE POINTS #####################################

# circle radius
r = 100
i = 0

# print on each point
for j in range(1,9): 
	for point in PointsInCircum(j*10*5, 10):
		# for y in range (j, j*-1):
		x = point[0]
		y = point[1]
		print(x,y)
		t.penup()
		t.setx(x+100)
		t.sety(y+100)
		t.pendown()
		# create_snowflake(1, 100)
		snowflake(random.randint(1, 3))
		# if (i%2 == 0):
		# 	create_snowflake(2, 100)
		# else:
		# 	snowflake(i%4) 

		# if (i==10):
		# 	break
		i = i+1





# for j in range(1,9): 
	# for point in PointsInCircum(j*10*5, 10):
		
# turtle.mainloop()
from datetime import datetime

now = datetime.now()
turtle.getcanvas().postscript(file=f"{now}-koch.eps")
