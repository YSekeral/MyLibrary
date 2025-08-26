from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, select

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

class Base(DeclarativeBase):
    pass



app = Flask(__name__)



app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new_books_data"

db = SQLAlchemy(model_class=Base)
db.init_app(app)





class Books(db.Model):
    __tablename__ = "books"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating : Mapped[float] = mapped_column(Float, nullable=False)


    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()



@app.route('/')
def home():
    result = db.session.execute(select(Books).order_by(Books.title))
    all_books = result.scalars().all()
    print(all_books)
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        new_book = Books(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=["GET","POST"])
def edit():
    if request.method == 'POST':
        book_id = request.form['id']
        book_to_update = db.get_or_404(Books, book_id)
        book_to_update.rating = float(request.form["rating"])
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Books, book_id)
    return render_template("edit_rating.html", book=book_selected)

@app.route("/delete")
def delete():
    target_id = request.args.get("id")
    book_to_delete = db.get_or_404(Books, target_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

