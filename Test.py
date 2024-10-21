import pytest
from fastapi.testclient import TestClient
from  APIs import app  # import your FastAPI app from main.py

client = TestClient(app)  # use TestClient to send requests

# Test for the create_book endpoint
def test_create_book():
    # Mock book data
    book_data = {
        "title": "Test Book",
        "author": "Author Name",
        "genre": "Fiction",
        "year_published": "2024",
        "summary": "This is a test summary."
    }

    # Send POST request to /books/ endpoint
    response = client.post("/books/", json=book_data)

    # Assert status code and response content
    if response.status_code !=200:
        pytest.fail(f"Expected status code 200, got {response.status_code}: {response.json()}")

    assert response.status_code == 200
    assert response.json()["message"] == "Book added successfully"
    assert "id" in response.json()

# Test for the get_books endpoint
def test_get_books():
    # Send GET request to /books/
    response = client.get("/books/")

    # Assert status code and response content
    if response.status_code !=200:
        pytest.fail(f"Expected status code 200, got {response.status_code}")

    assert response.status_code == 200
    assert "books" in response.json()  

# Test for getting book by id
def test_get_book_by_id():
    # First create a book to get its ID
    book_data = {
        "title": "Test Book",
        "author": "Author Name",
        "genre": "Fiction",
        "year_published": "2024",
        "summary": "This is a test summary."
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Now fetch the book by ID
    response = client.get(f"/books/{book_id}")
    if response.status_code !=200:
        pytest.fail(f"Expected status code is 200 but got {response.status_code}")
    assert response.status_code == 200
    assert response.json()["books"]["title"] == book_data["title"]

# Test for updating a book by id
def test_update_book_by_id():
    # First create a book
    book_data = {
        "title": "Test Book",
        "author": "Author Name",
        "genre": "Fiction",
        "year_published": "2024",
        "summary": "This is a test summary."
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Update the book's data
    updated_book_data = {
        "title": "Updated Book",
        "author": "Updated Author",
        "genre": "Non-Fiction",
        "year_published": "2025",
        "summary": "Updated summary."
    }

    response = client.put(f"/books/{book_id}", json=updated_book_data)
    if response.status_code !=200:
        pytest.fail(f"Expected status code is 200 but got {response.status_code}")
    assert response.status_code == 200
    assert response.json()["Updated Book"]["title"] == updated_book_data["title"]

# Test for deleting a book by id
def test_delete_book_by_id():
    # First create a book
    book_data = {
        "title": "Test Book",
        "author": "Author Name",
        "genre": "Fiction",
        "year_published": "2024",
        "summary": "This is a test summary."
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Now delete the book
    response = client.delete(f"/books/{book_id}")
    if response.status_code !=200:
        pytest.fail(f"Expected status code is 200 but got {response.status_code}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book has been deleted successfully"


# Test for adding a review
def test_add_review():
    # Create a book to review
    book_data = {
        "title": "Test Book",
        "author": "Author Name",
        "genre": "Fiction",
        "year_published": "2024",
        "summary": "This is a test summary."
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Review data
    review_data = {
        "user_id": 1,
        "review_text": "Great book!",
        "rating": 5
    }

    # Add review for the book
    response = client.post(f"/books/{book_id}/reviews/", json=review_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Book review added successfully"

# Test for getting reviews of a book
def test_get_reviews():
    # Create a book and add a review
    book_data = {
        "title": "Test Book",
        "author": "Author Name",
        "genre": "Fiction",
        "year_published": "2024",
        "summary": "This is a test summary."
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    review_data = {
        "user_id": 1,
        "review_text": "Great book!",
        "rating": 5
    }
    client.post(f"/books/{book_id}/reviews/", json=review_data)

    # Fetch reviews
    response = client.get(f"/books/{book_id}/reviews/")
    assert response.status_code == 200
    assert len(response.json()["Reviews"]) > 0

