from turtle import Turtle


coordinates = [(0,0),(-20,0),(-40,0)]
class Snake(Turtle):
    def __init__(self):
        self.segments = []
        self.create_field()

    def create_field(self):
        for i in range(0,len(coordinates)):
            new_segment = Turtle()
            new_segment.shape("square")
            new_segment.penup()
            new_segment.goto(coordinates[i])
            self.segments.append(new_segment)
    def move(self):
        for i in reversed(range(1,len(self.segments))):
            self.segments[i].goto(self.segments[i-1].position())
        self.segments[0].fd(20)
    def add_segment(self):
        new_segment = Turtle()
        new_segment.shape("square")
        new_segment.penup()
        new_segment.goto(self.segments[-1].position())
        self.segments.append(new_segment)
    def forward(self):
        self.segments[0].setheading(90)
    def left(self):
        self.segments[0].setheading(180)
    def right(self):
        self.segments[0].setheading(0)
    def backward(self):
        self.segments[0].setheading(270)
