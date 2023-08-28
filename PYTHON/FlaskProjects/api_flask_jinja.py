from flask import Flask
from flask import render_template
import requests

app = Flask(__name__)


@app.route('/')
def say_hello():
    return "Hello user!"

@app.route('/guess/<name>')
def guesser(name):
    api_call_gender = requests.get("https://api.genderize.io", params={"name": name})
    api_call_age = requests.get("https://api.agify.io/", params={"name": name})
    return render_template("index_blog.html", name = name, age = api_call_age.json()['age'], gender = api_call_gender.json()['gender'])


if __name__ == "__main__":
    app.run(debug=True)