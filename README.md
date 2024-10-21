# Book Management and Recommendation System

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements and Setup](#requirements-and-setup)
- [Llama3 Model Integration](#llama3-model-integration)
- [RESTful API and Asynchronous Programming](#restful-api-and-asynchronous-programming)
- [Cloud Deployment](#cloud-deployment)
- [Usage](#usage)

## Overview
This intelligent book management system leverages Python, a locally running Llama3 generative AI model, and cloud infrastructure to allow users to manage their library, generate summaries, and receive book recommendations tailored to their preferences.

## Features
- **Book Management**: Add, update, delete, and retrieve book details.
- **Book Summaries**: Automatically generate summaries for new books.
- **Review Management**: Add and retrieve reviews for books, along with an aggregated rating.
- **Recommendations**: Get personalized book recommendations based on user input.
- **Llama3 Integration**: Uses the Llama3 model for generating summaries and review insights.

Database:
Install PostgreSQL and connect it to the application.
Create the necessary tables using the .sql files provided in the db folder.
Update the credentials in the .env file with your database details.
Llama3 Model:
Download and install the Llama3 model from Ollama.
Set up the model within your virtual environment as explained below.
Llama3 Model Integration
Model Installation:
Install the Llama3 model by following instructions on Ollama’s official site.
After installation, pull the model into your virtual environment.
Model Interaction:
The model_inference.py file handles Llama3 model interaction using LangChain.
All interactions and performance logs are stored in model_interaction.logs.
Endpoints for Generating Summaries:
Generate Book and Review Summaries:
json
Copy code
POST http://127.0.0.1:8000/generate_book_and_review
Body: 
{
  "text": "Science Fiction"
}
This will generate a list of the top 5 books and their review summaries.

Generate New Book Summaries:
json
Copy code
POST http://127.0.0.1:8000/new_book_summary
Body: 
{
  "title": "Justice League",
  "author": "JK Rowling",
  "genre": "Fiction",
  "year_published": 1951,
  "summary": "A comic book about different heroes."
}
Authentication: To interact with these endpoints, use the authenticate_user function from APIs.py to get the required credentials.

RESTful API and Asynchronous Programming
The system uses FastAPI to interact with the database (PostgreSQL) asynchronously. Below are the primary API endpoints:

Add a New Book:
json
Copy code
POST /books
Body:
{
  "title": "Justice League",
  "author": "JK Rowling",
  "genre": "Fiction",
  "year_published": 1951,
  "summary": "A comic book story."
}
Retrieve All Books:
bash
Copy code
GET /books
Retrieve a Specific Book by ID:
bash
Copy code
GET /books/{id}
Update Book Information:
json
Copy code
PUT /books/{id}
Body: 
{
  "title": "Where the Crawdads Sing",
  "author": "Delia Owens",
  "genre": "Mystery, Fiction, Comedy",
  "year_published": 2018,
  "summary": "A coming-of-age story combined with a murder mystery."
}
Delete a Book:
bash
Copy code
DELETE /books/{id}
Add a Review to a Book:
json
Copy code
POST /books/{id}/reviews
Body: 
{
  "user_id": "123",
  "review_text": "This book is amazing!",
  "rating": 4
}
Retrieve All Reviews for a Book:
bash
Copy code
GET /books/{id}/reviews
Get Book Summary and Ratings:
bash
Copy code
GET /books/{id}/summary
Get Book Recommendations Based on User Preferences:
json
Copy code
GET /recommendations
Body: 
{
  "text": "Sapiens: A Brief History of Humankind"
}
Cloud Deployment
PostgreSQL Configuration:
Update the PostgreSQL connection settings from localhost to the cloud server.
Secure APIs:
Ensure secure communication by changing the domain from local to the cloud instance.
Deployment:
Push the code to the deployment server.
Run the FastAPI server using:
bash
Copy code
uvicorn API:app --reload
Usage
Local Development:
Create a virtual environment and install dependencies:
bash
Copy code
pip install -r requirements.txt
Run the FastAPI server:
bash
Copy code
uvicorn API:app --reload
Testing:
A test.py file is provided to easily test all API endpoints and database interactions.
Authentication is required for API access. Use the following basic authentication:
Username: <user_name>
Password: <password>
