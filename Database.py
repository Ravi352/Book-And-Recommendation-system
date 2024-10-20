from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

from model_inference import *
# Create the FastAPI instance
app = FastAPI()

# PostgreSQL connection parameters
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Books"
DB_USER = "postgres"
DB_PASS = "Ravi@123"  # Replace with your actual password

# Define the Book model for the validation to avoid validation each time
class Book(BaseModel):
    title: str
    author: str
    genre:str
    year_published:str
    summary:str

class Review(BaseModel):
    user_id: int
    review_text:str
    rating:int

class Text(BaseModel):
    text:str

class recommendation_request(BaseModel):
    user_id:int


def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn


@app.post("/books/")
async def create_book(book: Book):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO books (title, author, genre, year_published, summary) VALUES (%s, %s, %s,%s,%s) RETURNING id;",
            (book.title, book.author, book.genre, book.year_published,book.summary)
        )

        book_id = cursor.fetchone()[0]
        conn.commit()
        return {"id": book_id, "message": "Book added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@app.get("/books/")
async def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM books;",
        )
        books = cursor.fetchall()
        book_list = []
        for book in books:
            book_list.append(
                {
                    "ID":book[0],
                    'title':book[1],
                    'author':book[2],
                    'genre':book[3],
                    "year_published":book[4],
                    "summary":book[5],

                }
                )
        return {'Books':book_list}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/books/{id}")
async def get_book_by_id(id:str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select id from books where id=%s",(id,))
        books_exist = cursor.fetchone()
        print("books_exist",books_exist)
        if books_exist is None:
            print("coming here in this")
            raise HTTPException(status_code=404, detail="Book not found")
        cursor.execute(
            "SELECT title, author,genre,year_published,summary  FROM books where id=%s;",(id,),
        )
        book = cursor.fetchone()
        book = {
            'title':book[0],
            'author':book[1],
            'genre':book[2],
            "year_published":book[3],
            "summary":book[4],
        }
        return {'Books':book}
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=404, detail=str("The Book id is not present in the Database. Please check the book id"))
    finally:
        cursor.close()
        conn.close()


@app.put("/books/{id}")  # Use PUT for updates
async def update_book_by_id(id: str, book: Book):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select id from books where id=%s",(id,))
        books_exist = cursor.fetchone()
        print("books_exist",books_exist)
        if books_exist is None:
            print("coming here in this")
            raise HTTPException(status_code=404, detail="Book not found")
        
        cursor.execute(
            """
            UPDATE books 
            SET title = %s, author = %s, genre = %s, year_published=%s, "summary"=%s
            WHERE id = %s;
            """,
            (book.title, book.author, book.genre, book.year_published, book.summary, int(id))
        )
        
        # Check if any rows were updated
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Book not found")
        
        conn.commit()
        return {"message": "Book updated successfully","Updated Book":book}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=404, detail=str("Book is not found"))
    
    finally:
        cursor.close()
        conn.close()


@app.delete("/books/{id}")  # Use PUT for updates
async def delete_book_by_id(id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select id from books where id=%s",(id))
        books_exist = cursor.fetchone()
        print("books_exist",books_exist)
        if books_exist is None:
            # print("coming here in this")
            raise HTTPException(status_code=404, detail="Book not found")
        
        cursor.execute(
            """
            DELETE from books
            WHERE id = %s;
            """,(id)
        )
        # Check if any rows were updated
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Book not found")
        
        conn.commit()
        return {"message": "Book has been deleted successfully"}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=404, detail=str("Book is not found"))
    
    finally:
        cursor.close()
        conn.close()


"""" Reviews"""


@app.post("/books/{id}/reviews/")
async def add_review(id: str, review: Review):
    conn = get_db_connection()
    cursor = conn.cursor()
    try: 
        # Check if the book exists
        cursor.execute("SELECT id FROM books WHERE id = %s", (id,))
        book_exists = cursor.fetchone()
        print("Book exists",book_exists)
        if book_exists is None:
            raise HTTPException(status_code=404, detail="Book does not exist")

        # Insert the review into the book_reviews table
        cursor.execute(
            "INSERT INTO book_reviews (book_id,user_id, review_text, rating) VALUES (%s,%s, %s, %s) RETURNING id;",
            (id,review.user_id, review.review_text, review.rating)
        )
        review_id = cursor.fetchone()[0]
        conn.commit()

        return {"id": review_id, "message": "Book review added successfully"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Book does not exist")
    finally:
        conn.close()

        
@app.get("/books/{id}/reviews/")
async def add_review(id: str):
    conn = get_db_connection()
    cursor = conn.cursor() 
    try:
        # get all the reviews from the book_reviews table
        cursor.execute(
            "SELECT review_text from book_reviews where book_id= %s",(id,),
        )
        reviews = cursor.fetchall()
        total_review = []
        for review in reviews:
            total_review.append(review)

        return {"Reviewer_id":id,"Reviews":total_review}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Book does not exist")
    finally:
        conn.close()



@app.get("/books/{id}/summary/")
async def add_review(id: str):
    conn = get_db_connection()
    cursor = conn.cursor() 
    try:
        cursor.execute("SELECT id FROM books WHERE id = %s", (id,))
        book_exists = cursor.fetchone()
        print("Book exists",book_exists)
        if book_exists is None:
            raise HTTPException(status_code=404, detail="Book does not exist")

        cursor.execute(
            "SELECT avg(rating) from book_reviews where book_id= %s",(id,),
        )
        rating = cursor.fetchone()[0]
        cursor.execute(
            "SELECT review_text from book_reviews where book_id= %s",(id,),
        )
        all_reviews = cursor.fetchall()
        print(all_reviews)
        reviews = [review[0] for review in all_reviews]
        inputs = ' '.join(reviews)
        # print(inputs)
        # print("rating",rating,"Reviews",reviews)
        summary = get_summary(inputs)
        return {"Rating":round(rating,2),"Summary of Reviews":summary}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Book does not exist")
    finally:
        conn.close()


@app.post("/generate-summary/")
async def generate_summary_(input:Text):
    content = input.text
    print("----->",content)
    output = generate_summary(content)
    return {"Summary":output}


@app.get("/recommendations/")
async def get_recommendation(user_id:recommendation_request):
    print("---->",user_id.user_id)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM book_reviews WHERE user_id = %s", (user_id.user_id,))
        user_exist = cursor.fetchall()
        if not user_exist:
            raise HTTPException(status_code=404,detail="User did not found")
        rating = []
        review = []
        book_ids = set()
        for data in user_exist:
            if data[4]>2:
                book_ids.add(data[1])
                review.append(data[3])
                rating.append(data[4])
        print(rating,review,book_ids)
        genres = []
        for value in book_ids:
            cursor.execute("SELECT genre from books where id=%s",(value,))
            genre= cursor.fetchall()[0]
            genres.append(genre)
        all_genres = [genre[0] for genre in genres ]
        inputs = ' '.join(all_genres)
        recommendation = generate_recommendation(inputs)
        
        return {"Top Recommendation for the user":recommendation}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=404, detail="User did not found")
    finally:
        conn.close()





