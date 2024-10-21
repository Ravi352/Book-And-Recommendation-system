# Book-And-Recommendation-system

Table of Contents
* Overview
* Features
* Requirements and Database Setup
* Llama3 Model Integration
* RESTful API and Asynchronous Programming
* Cloud Deployment
* Usage

## Overview 
This intelligent book management system is built using Python, a locally running Llama3 generative AI model, and cloud infrastructure. The system enables users to manage a library of books, generate summaries, and receive recommendations based on user preferences.

## Requirements 

To running the properly locally, create a new environment into the vscode and install all the dependencies using requirement.txt file, install PostgreSql and connect it with database.
Create a tables on the database with the queries .sql files from the data given above. Sign in with the database with the credentials which is mentioned in the database.env. 


## Llama3 Model Integration

Install the Ollama3 model from the official website "https://ollama.com/". Take the model and install in the system, after installing it pull the the model into the your virtual environment. The model interaction and integration with langchain is implmented in the model_inference.py file. The logger is set to track all the logs (model_interaction.logs) of the model interations with time taken by the model for the given query.

Generating book and review summeries: You have to the topic of the book and it will generate top 5 books and its review summary.
#### POST "http://127.0.0.1:8000/generate_book_and_review"
body: {
        "text":"Science Fiction"
    }

To Use this endpoint You will be needed authentication the credentials you can get from the "authenticate_user" function in the APIs.py. 

Generate summaries for new book entries and review summaries.
#### POST "http://127.0.0.1:8000/new_book_summary"

body:  {
          "title": "Justice League",
          "author": "JK Rolling",
          "genre": "Fiction",
          "year_published": 1951,
          "summary": "A comic book of diiferent heros"
        }


## RESTful API and Asynchronous Programming
APIs.py file created to interact with model and contains all the APIs which is used to interact with the database (postgresql). The operations and the methods are mentioned below. for local instance the initial endpoints would be "http://127.0.0.1:8000/{Variable}". Variable is the endpoint(e.g.  /books, /books/id) the values as given below with the respective method and inputs (JSON body) to check the APIs are given below: 

#### POST /books: Add a new book.
body : {
          "title": "Justice League",
          "author": "JK Rolling",
          "genre": "Fiction",
          "year_published": 1951,
          "summary": "A comic book story"
          }

#### GET /books: Retrieve all books.
    No Parameters Required just send the request and results will appeared.
#### GET /books/<id>: Retrieve a specific book by its ID.
    No Parameters Required just send the request and results will appeared
#### PUT /books/<id>: Update a book's information by its ID.
    {
    "title": "Where the Crawdads Sing",
    "author": "Delia Owens",
    "genre": "Mystery, Fiction,comedy",
    "year_published":"2018",
    "summary":"A coming-of-age story combined with a murder mystery about Kya Clark, the Marsh Girl, set in a small North Carolina town."
    }

#### DELETE /books/<id>: Delete a book by its ID.
    No Parameters Required just send the request and results will appeared
  
#### POST /books/<id>/reviews: Add a review for a book.
    {
    "user_id":"123",
    "review_text":"This book is better than the other books what I have read",
    "rating":4
    }
  
#### GET /books/<id>/reviews: Retrieve all reviews for a book.
    No Parameters Required just send the request and results will appeared
    
#### GET /books/<id>/summary: Get a summary and aggregated rating for a book.
    No Parameters Required just send the request and results will appeared
  
#### GET /recommendations: Get book recommendations based on user preferences.
    {
    "text":"Sapiens: A Brief History of Humankind by Yuval Noah Harari"
    }

#### POST /generate-summary: Generate a summary for a given book content.

    {
    "user_id":123
    }

SQLAlchemy is used to interact with the postgresql so that it can handle multiple request without any restriction. 


## Cloud Deployment 

changes are needed in the PostgreSql, change the local host to the server in which the deployment shoud be done. Stabilish a secure connection with APIs by changing the domain from local to the instance.
After push the code to the deployment server and run the fast api server.


## Usage

Open the terminal and create virtual environment. install all the dependencies in the server. Run "uvicorn APIs:app --reload" so that the fast api server will start and all the APIs can be tested.
To check if the all APIs are working correctly "test.py" file is given in the code. It can easily test all the APIs endpoints and database interaction. 

One authenication will be required to every api for the authenticity, which is a basic authentication and can be set user:"user_name", password:"Password". if you are using postman for checking the apis go to authentication in the postman and fill the username and password after that only you can access the APIs.
