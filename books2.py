from operator import gt
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

BOOKS = []  

class Book:
    id: int
    title: str
    author: str
    description: str
    rating : int
    published: int

    def __init__(self,id, title, author, description, rating, published):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published = published

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='Optional Field for create',default=None)
    title: str = Field(min_lengnth=3)
    author: str = Field(min_lengnth=1)
    description: str = Field(min_lengnth=3, max_length=1000)
    rating : int = Field(gt=1, lt=6)
    published: int = Field(gt=1600)
   
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The guide",
                "author": "Narayan R. K.",
                "description": "The Guide is a 1958 novel written in English by the Indian author R. K. Narayan.\
 Like most of his works, the events of this novel take place in Malgudi, a fictional town in South India. ",
                "rating": 5,
                "published": 1958
            }
        }
    }

BOOKS = [
    Book(1,'cse','auth','descrition1',4,2012),
    Book(2,'cse','auth2','descrition2',3,2013),
    Book(3,'cse','auth3','descrition3',2,2014),
    Book(4,'cse','auth4','descrition4',1,2014),
    Book(5,'cse','auth5','descrition5',5,2015),
]



@app.get('/books')
def read_all_books():
    return BOOKS

@app.get("/books/{book_rating}")
def get_book_by_rating(book_rating: int):
    for book in BOOKS:
        book_to_return=[]
        if book.rating==book_rating:
            book_to_return.append(book)
    return book_to_return

@app.put("/books/update-book")
def update_book(update_book: BookRequest):
    for book in BOOKS:
        if book.id == update_book.id:
            BOOKS[book.id]=update_book
    return BOOKS

@app.post("/create-book")
def create_book(new_book: BookRequest):
    new_book = Book(**new_book.model_dump())
    BOOKS.append(create_book_id(new_book))
    return BOOKS

@app.get("/get_book{book_id}")
def fetch_book(book_id: int):
    return BOOKS[book_id-1]

@app.delete("/books/{book_id}")
def delete_a_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.pop(book_id-1)
    return BOOKS

@app.get("/books/")
def get_book_by_year(published: int):
    for book in BOOKS:
        if book.published == published:
            return book

def create_book_id(book:Book):
    if len(BOOKS)>=0:
        book.id=len(BOOKS)
    else:
        book.id=1
    return book