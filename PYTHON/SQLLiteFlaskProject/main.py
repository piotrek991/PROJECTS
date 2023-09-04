from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, FloatField
from wtforms.validators import DataRequired,Email,Length
from flask_sqlalchemy import SQLAlchemy as sa
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///new-books-collection.db'
db = sa()
db.init_app(app)

class add_book_form(FlaskForm):
    author = StringField(label="Book Author",validators=[DataRequired()])
    title = StringField(label="Book title", validators=[DataRequired()])
    rating = FloatField(label = "Rating", validators=[DataRequired()])
    add_butt = SubmitField(label = "Add book")

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,unique = True, nullable = False)
    author = db.Column(db.String, nullable = False)
    rating = db.Column(db.Float,nullable = False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    result = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = result.scalars()
    return render_template("index.html", books = all_books)


@app.route("/add", methods = ["POST","GET"])
def add():
    book_form = add_book_form()
    if book_form.validate_on_submit():
        if request.method == "POST":
            new_book = Books(
            title = book_form.title.data
            , author=book_form.author.data
            , rating=book_form.rating.data
            )
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form = book_form)


if __name__ == "__main__":
    app.run(debug=True)

