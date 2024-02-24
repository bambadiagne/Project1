import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))
db = scoped_session(sessionmaker(bind=engine))

with open("books.csv") as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for isbn,title,author,year in reader:
        print(year)
        db.execute("INSERT INTO books (isbn, title_book, author_book, year_book) VALUES (:isbn,:title_book,:author_book,:year_book)",{"isbn": isbn, "title_book": title, "author_book": author,"year_book": year})
        db.commit()

