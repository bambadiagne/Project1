\c mydatabase;
CREATE TABLE books (
    id_book SERIAL PRIMARY KEY,
    isbn VARCHAR(10),
    title_book VARCHAR(255),
    author_book VARCHAR(255),
    year_book INT
);
CREATE TABLE users (    
    id_user SERIAL PRIMARY KEY,
    username VARCHAR(255),
    passwd VARCHAR(255),
    email VARCHAR(255)
);
CREATE TABLE reviews (
    id_review SERIAL PRIMARY KEY,
    comments TEXT,
    rating INT,
    id_user INT,
    isbn VARCHAR(10),
    FOREIGN KEY (id_user) REFERENCES users (id_user)
);
