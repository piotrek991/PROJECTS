from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def say_hello():
    return render_template("index.html")

@app.route('/login', methods=["POST"])
def receive_data():
    login_text = request.form.get("lname")
    password_text = request.form.get("fname")
    return render_template("login.html", login = login_text, password = password_text)

if __name__ == "__main__":
    app.run(debug=True)