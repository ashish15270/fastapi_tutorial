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

    def __init__(self,id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='Optional Field for create',default=None)
    title: str = Field(min_lengnth=3)
    author: str = Field(min_lengnth=1)
    description: str = Field(min_lengnth=3, max_length=1000)
    rating : int = Field(gt=1, lt=6)
   
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The guide",
                "author": "Narayan R. K.",
                "description": "The Guide is a 1958 novel written in English by the Indian author R. K. Narayan.\
 Like most of his works, the events of this novel take place in Malgudi, a fictional town in South India. ",
                "rating": 5
            }
        }
    }

BOOKS = [
    Book(1,'cse','auth','descrition1',4),
    Book(2,'cse','auth2','descrition2',4),
    Book(3,'cse','auth3','descrition3',4),
    Book(4,'cse','auth4','descrition4',4),
    Book(5,'cse','auth5','descrition5',4),
]



@app.get('/books')
def read_all_books():
    return BOOKS

@app.post("/create-book")
def create_book(new_book: BookRequest):
    new_book = Book(**new_book.model_dump())
    BOOKS.append(find_book_id(new_book))
    return BOOKS

@app.get("/get_book{book_id}")
def fetch_book(book_id: int):
    return BOOKS[book_id-1]

def find_book_id(book:Book):
    if len(BOOKS)>=0:
        book.id=len(BOOKS)
    else:
        book.id=1
    return book