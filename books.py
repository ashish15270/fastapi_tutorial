from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = {
    "1": {
        "title": "Book 1",
        "author": "Author 1",
        "category": "Category 1"
    },
    "2": {
        "title": "Book 2",
        "author": "Author 2",
        "category": "Category 1"
    },
    "3": {
        "title": "Book 1",
        "author": "Author 1",
        "category": "Category 5"
    },
    "4": {
        "title": "Book 2",
        "author": "Author 2",
        "category": "Category 2"
    }
}

@app.get("/books")
async def read_all_books_by_category(category: str):
    books_to_return = []
    for book in BOOKS.values():
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_id}")
async def read_all_books(book_id: str):
    return BOOKS[book_id]

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS[str(len(BOOKS) + 1)] = new_book
    return BOOKS

@app.put("/books/update_book/{book_id}")
async def update_book(book_id: str, new_book=Body()):
    for book_id, book in BOOKS.items():
        if book_id == book_id:
            BOOKS[book_id] = new_book
    return BOOKS[book_id]

@app.delete("/books/delete_book/{book_id}")
async def delete_book(book_id: str):
    del BOOKS[book_id]
    return BOOKS