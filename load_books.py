import csv, sqlalchemy, os
 
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
 
with open('books.csv') as data:
    reader = csv.reader(data)
    next(reader, None) #skip headers
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {'isbn':isbn, 'title':title, 'author':author, 'year':year})
        db.commit()