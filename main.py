from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Books %r>' % self.title


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # new_book = Books(id=2, title="Harry sdfr", author="J.sadng", rating=9.3)
        # CREATE RECORD
        new_book = Books(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    book_to_update = Books.query.get(id)
    if request.method == 'POST':
        print(f'Old_book_rating: {book_to_update.rating}')
        rating = request.form['rating']
        book_to_update.rating = rating
        print(f'User_rating: {rating}')
        print(f'New_book_rating: {book_to_update.rating}')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", book=book_to_update)


@app.route('/delete', methods=['GET'])
def delete():
    book_id = request.args.get('id')
    book_to_delete = Books.query.get(book_id)
    print(book_to_delete.title)
    if request.method == 'GET':
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for('home'))




if __name__ == "__main__":
    app.run(debug=True)

