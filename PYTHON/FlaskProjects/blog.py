from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

@app.route('/')
def home():
    date = datetime.now()
    return render_template("blog.html",year = date.year)

@app.route('/blog')
def blog():
    all_post = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
    return render_template("blog.html", posts = all_post)

if __name__ == "__main__":
    app.run(debug=True)