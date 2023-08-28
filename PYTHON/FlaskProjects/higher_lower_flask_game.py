from flask import Flask
import random

app = Flask(__name__)
random_number = random.randint(0,10)

@app.route('/')
def hello():
    return '<h1>Number guesser game</h1>' \
           '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif">'

@app.route('/<int:guess>')
def say_hello(guess):
    if guess < random_number:
        return '<h1>its to low try again</h1>' \
               '<img src = "https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif">'
    elif guess > random_number:
        return '<h1>its to high try again</h1>' \
               '<img src = "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif">'
    else :
        return '<h1>Its correct</h1>' \
               '<img src = "https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif">'

if __name__ == "__main__":
    app.run(debug= True)



