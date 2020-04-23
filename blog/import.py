import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

with open("books.csv") as f:
    reader = csv.reader(f)
    for isbn,title,author,year in reader:
        db.execute("INSERT INTO books (isbn, title_book, author_book, year_book) VALUES (:isbn,:title_book,:author_book,:year_book)",{"isbn": isbn, "4title_book": title, "author_book": author,"year_book": year})
        db.commit()

