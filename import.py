import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))

#engine = create_engine("postgresql://postgres:password@localhost/project1")
#edit remove os.getenv funtion in create_engine()
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    c=0
    for isbn,title,author,year in reader:
        db.execute("INSERT INTO books (isbn, title, author,year) VALUES (:isbn, :title, :author,:year)",
                    {"isbn":isbn, "title":title, "author":author,"year":year})
        #print(f"Added flight from {origin} to {destination} lasting {duration} minutes.")
        c=c+1
    print(c)
    db.commit()

if __name__ == "__main__":
    main()
