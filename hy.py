from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from typing import List

app = FastAPI()
engine = create_engine("sqlite+pysqlite:///books.db")
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    title = Column(String)
    language = Column(String)
    genre = Column(String)
    cover = Column(String)
    translated_text = Column(String)
    audioW = Column(String, default="female voice")
    audioM = Column(String, default="male voice")
    price = Column(Integer)

Base.metadata.create_all(engine)

class BookResponse(BaseModel):
    id: int
    text: str
    title: str
    language: str
    cover: str
    translated_text: str
    audioW: str
    audioM: str
    price: int

@app.get("/book/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    session = Session()
    book = session.query(Book).filter(Book.id == book_id).first()
    session.close()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return BookResponse(**book.__dict__)


@app.get("/books/by_genre/{genre}", response_model=List[BookResponse])
def get_books_by_genre(genre: str):
    session = Session()
    books = session.query(Book).filter(Book.genre == genre).all()
    session.close()
    if not books:
        return []

    return [BookResponse(**book.__dict__) for book in books]


@app.get("/books/by_id/{book_id}", response_model=List[BookResponse])
def get_books_by_id(book_id: int):
    session = Session()
    books = session.query(Book).filter(Book.id == book_id).all()
    session.close()
    if not books:
        return []

    return [BookResponse(**book.__dict__) for book in books]

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)