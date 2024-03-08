from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

# all_books = []
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = result.scalars()
        return render_template("index.html", books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        with app.app_context():
            new_book = Book(title=request.form['name'], author=request.form['author'], rating=request.form['rating'])
            db.session.add(new_book)
            db.session.commit()
        # new_book = {
        #     'title': request.form['name'],
        #     'author': request.form['author'],
        #     'rating': request.form['rating']
        # }
        # all_books.append(new_book)
    return render_template("add.html")


@app.route("/update/<book_id>", methods=['POST', 'GET'])
def update(book_id):
    # if request.method != "POST":
    #     with app.app_context():
    #         book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    #         return render_template("update.html", book=book_to_update)
    # else:
    #     with app.app_context():
    #         book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    #         book_to_update.rating = request.form['rating']
    #         db.session.commit()
    #         book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    #         return render_template("update.html", book=book_to_update)
    with app.app_context():
        book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        if request.method == "POST":
            book_to_update.rating = request.form['rating']
            db.session.commit()
        book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        return render_template("update.html", book=book_to_update)






if __name__ == "__main__":
    app.run(debug=True)

