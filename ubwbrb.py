import base64
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session, joinedload
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)  # Correct initialization using __name__
engine = create_engine("sqlite+pysqlite:///books.db")
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))

class Book(Base):
    __tablename__ = 'books'  # Correct attribute name for tablename
    id = Column(Integer, primary_key=True)
    text = Column(String)
    title = Column(String)
    language = Column(String)
    genre = Column(String)  # Added genre field
    cover = Column(String)
    translated_text = Column(String)
    audioW = Column(String, default="female voice")
    audioM = Column(String, default="male voice")
    price = Column(Integer)

Base.metadata.create_all(engine)
x=['1','2'
]
@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    session = Session()
    book = session.query(Book).filter(Book.id == book_id).first()
    session.close()
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    response = jsonify({
        'id': book.id,
        'text': book.text,
        'title': book.title,
        'language': book.language,
        'cover': x[0],
        'translated_text': book.translated_text,
        'audioW': x[1],
        'audioM': x[1],
        'price': book.price
    })
    return response

@app.route('/books/by_genre/<string:genre>', methods=['GET'])
def get_books_by_genre(genre):
    session = Session()
    books = session.query(Book).filter(Book.genre == genre).all()
    session.close()
    if not books:
        return jsonify([])
    return jsonify([{'id': b.id, 'title': b.title, 'cover': b.cover, 'price': b.price, 'translated_text': b.translated_text} for b in books])

@app.route('/books/by_id/<int:book_id>', methods=['GET'])
def get_books_by_id(book_id):
    session = Session()
    books = session.query(Book).filter(Book.id == book_id).all()
    session.close()
    if not books:
        return jsonify([])
    return jsonify([{'id': b.id, 'title': b.title, 'cover': b.cover, 'price': b.price, 'translated_text': b.translated_text} for b in books])

if __name__ == '__main__':
    app.run(debug=True)
