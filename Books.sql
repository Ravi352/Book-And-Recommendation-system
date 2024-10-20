CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    year_published INT CHECK (year_published > 0),  -- Ensure the year is a positive number
    summary TEXT
);


