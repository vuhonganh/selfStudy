import turtle

def draw_square(some_turtle):	
	for i in range(1, 5):
		some_turtle.forward(200)	
		some_turtle.right(90)	
	


def draw_art():
	window = turtle.Screen()
	brad = turtle.Turtle()
	brad.speed(10)
	angle = 10
	for i in range(1, 360/angle):
		draw_square(brad)
		brad.right(angle)

	window.exitonclick()


draw_art()