import time
import turtle as t
from snake import Snake
from food import Food

screen = t.Screen()
screen.screensize(400,400)
screen.tracer(0)

snake = Snake()
food = Food()

screen.update()
screen.listen()
screen.onkey(snake.forward,"w")
screen.onkey(snake.backward,"s")
screen.onkey(snake.left,"a")
screen.onkey(snake.right,"d")

game_on = True
while game_on:
    snake.move()
    if snake.segments[0].distance(food)<20:
        print("NOM NOM")
        snake.add_segment()
        food.new_cord()
    screen.update()
    time.sleep(0.5)
screen.exitonclick()
