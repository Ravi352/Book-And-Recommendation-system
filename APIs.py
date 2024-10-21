from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import os
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float,func
from sqlalchemy.future import select
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from model_inference import *
import logging

logger = logging.getLogger(__name__)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# Create the FastAPI instance
app = FastAPI()
load_dotenv("database.env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print('----->',DATABASE_URL)
# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Define the SQLAlchemy Base model
Base = declarative_base()

class BookModel(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year_published = Column(Integer,nullable=False)  # Use appropriate type for date
    genre = Column(String)
    summary = Column(String)
    # Relationship with BookReview
    reviews = relationship('ReviewModel', back_populates='book')

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author}, genre={self.genre})>"


class ReviewModel(Base):
    __tablename__ = 'book_reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)

    # Relationship back to Book
    book = relationship('BookModel', back_populates='reviews')

    def __repr__(self):
        return f"<BookReview(id={self.id}, book_id={self.book_id}, user_id={self.user_id}, rating={self.rating})>"
    

# Define a Pydantic model for book data
class Book(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: str

    class Config:
        orm_mode = True  # This allows the Pydantic model to work with SQLAlchemy models

class Review(BaseModel):
    user_id: int
    review_text:str
    rating:int

    class Config:
        orm_mode = True

class Text(BaseModel):
    text:str

class recommendation_request(BaseModel):
    user_id:int



async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

security = HTTPBasic()
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = "postgres"
    correct_password = "Ravi@123"
    if credentials.username != correct_user or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.post("/books/", dependencies=[Depends(authenticate_user)])
async def create_book(book: Book, db: Session = Depends(get_db)):
    try:
        print("---->", book)
        db_book = BookModel(title=book.title, author=book.author, genre=book.genre, year_published=book.year_published, summary=book.summary)
        db.add(db_book)  # Adding SQLAlchemy model to session
        await db.commit()  # Use await with async session
        await db.refresh(db_book)  # Refresh to get the id
        return db_book
    except Exception as e:
        logger.exception("Error occurred while creating a book: %s", e)
        raise HTTPException(status_code=500, detail="An error occurred while creating the book.")
    


@app.get("/books/", summary="Get the books from the database",dependencies=[Depends(authenticate_user)])
async def get_books(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(BookModel))
        books = result.scalars().all()

        book_list = [
            {
                "ID": book.id,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                "year_published": book.year_published,
                "summary": book.summary,
            }
            for book in books
        ]
        return {'Books': book_list}
    except Exception as e:
        logger.exception("Error fetching books: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/books/{id}", summary="Get the book by ID", description="Retrieve the details of the book by its ID",dependencies=[Depends(authenticate_user)])
async def get_book_by_id(id: str, db: AsyncSession = Depends(get_db)):
    try:
        book = await db.get(BookModel, int(id))
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return {
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            "year_published": book.year_published,
            "summary": book.summary,
        }
    except Exception as e:
        logger.exception("Error fetching book by ID: %s", e)
        raise HTTPException(status_code=404, detail="The Book ID is not present in the Database. Please check the book ID")
    

@app.delete("/books/{id}", summary="Deletion of Book by ID", description="The book will be deleted from the database",dependencies=[Depends(authenticate_user)])
async def delete_book_by_id(id: str, db: AsyncSession = Depends(get_db)):
    try:
        db_book = await db.get(BookModel, int(id))
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")

        await db.delete(db_book)
        await db.commit()
        return {"message": "Book has been deleted successfully"}
    except Exception as e:
        logger.exception("Error deleting book: %s", e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Book not found")
    



@app.post("/books/{id}/reviews/", summary="Add the Review", description="Add the review for a book")
async def add_review(id: str, review: Review, db: AsyncSession = Depends(get_db)):
    try:
        book = await db.get(BookModel, int(id))
        if not book:
            raise HTTPException(status_code=404, detail="Book does not exist")

        db_review = ReviewModel(book_id=int(id), user_id=review.user_id, review_text=review.review_text, rating=review.rating)
        db.add(db_review)
        await db.commit()
        await db.refresh(db_review)
        return {"id": db_review.id, "message": "Book review added successfully"}
    except Exception as e:
        logger.exception("Error adding review: %s", e)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Book does not exist")
    

@app.get("/books/{id}/reviews/", summary="Get all reviews for a book", description="Returns the list of reviews of the book")
async def get_reviews(id: str, db: AsyncSession = Depends(get_db)):
    try:
        reviews = await db.execute(select(ReviewModel).filter_by(book_id=int(id)))
        reviews_list = reviews.scalars().all()

        if not reviews_list:
            raise HTTPException(status_code=404, detail="No reviews found")

        review_texts = [review.review_text for review in reviews_list]
        return {"Reviewer_id": id, "Reviews": review_texts}
    except Exception as e:
        logger.exception("Error fetching reviews: %s", e)
        raise HTTPException(status_code=500, detail="Book does not exist")


@app.get("/books/{id}/summary/", summary="Get summary of the book by ID", description="Get the average rating and summary of reviews")
async def get_average_rating_review(id: str, db: AsyncSession = Depends(get_db)):
    try:
        book = await db.get(BookModel, int(id))
        if not book:
            raise HTTPException(status_code=404, detail="Book does not exist")

        avg_rating = await db.execute(select(func.avg(ReviewModel.rating)).filter_by(book_id=int(id)))
        avg_rating = avg_rating.scalar()

        reviews = await db.execute(select(ReviewModel.review_text).filter_by(book_id=int(id)))
        reviews_list = reviews.scalars().all()

        summary = get_summary(' '.join(reviews_list))
        return {"Rating": round(avg_rating, 2), "Summary of Reviews": summary}
    except Exception as e:
        logger.exception("Error fetching summary: %s", e)
        raise HTTPException(status_code=500, detail="Book does not exist")


@app.post("/generate-summary/",summary="Generate summary of the book content",description="Will return the precise summary of the content",dependencies=[Depends(authenticate_user)])
async def generate_summary_(input:Text):
    content = input.text
    print("----->",content)
    output = generate_summary(content)
    return {"Summary":output}


@app.get("/recommendations/", summary="Recommendation for the user", description="Returns recommended books based on rating, review, and genres",dependencies=[Depends(authenticate_user)])
async def get_recommendation(user_id: recommendation_request, db: AsyncSession = Depends(get_db)):
    try:
        user_reviews = await db.execute(select(ReviewModel).filter_by(user_id=user_id.user_id))
        user_reviews = user_reviews.scalars().all()

        if not user_reviews:
            raise HTTPException(status_code=404, detail="User not found")

        # Filter reviews with rating > 2
        recommended_books = {review.book_id for review in user_reviews if review.rating > 2}
        genres = []
        for book_id in recommended_books:
            book = await db.get(BookModel, int(book_id))
            genres.append(book.genre)

        all_genres = ' '.join(genres)
        recommendation = generate_recommendation(all_genres)
        return {"Top Recommendations for the user": recommendation}
    except Exception as e:
        logger.exception("Error fetching recommendations: %s", e)
        raise HTTPException(status_code=500, detail="User not found")
