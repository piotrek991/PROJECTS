from flask import Flask
from flask_sqlalchemy import SQLAlchemy as sa

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///new-books-collection.db'
db = sa()
db.init_app(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,unique = True, nullable = False)
    author = db.Column(db.String, nullable = False)
    rating = db.Column(db.Float,nullable = False)

with app.app_context():
    db.create_all()

with app.app_context():
    new_book = Books(title="Harry Potter3", author="J. K. Rowling", rating=9.3)
    db.session.add(new_book)
    db.session.commit()

with app.app_context():
    result = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = result.scalars()
    print(all_books)





