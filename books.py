from fastapi import FastAPI

app = FastAPI()

BOOKS = {
    "1": {
        "title": "Book 1",
        "author": "Author 1"
    },
    "2": {
        "title": "Book 2",
        "author": "Author 2"
    }
}

@app.get("/books")
async def read_all_books():
    return BOOKS