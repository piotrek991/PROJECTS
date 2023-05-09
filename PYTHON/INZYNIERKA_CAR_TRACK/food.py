from turtle import Turtle
from snake import Snake
import random

class Food(Turtle):
    def __init__(self):
        super().__init__()
        rand_x = fruit_cords[random.randint(0,len(fruit_cords)-1)]
        rand_y = fruit_cords[random.randint(0,len(fruit_cords)-1)]
        self.shape("circle")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.goto(rand_x, rand_y)

    def new_cord(self):
        rand_x = fruit_cords[random.randint(0, len(fruit_cords) - 1)]
        rand_y = fruit_cords[random.randint(0, len(fruit_cords) - 1)]
        self.goto(rand_x,rand_y)

fruit_cords = []
for i in range(-400,401,20):
    fruit_cords.append(i)
