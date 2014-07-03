from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("sqlite:///ratings.db", echo=False)
dbsession = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = dbsession.query_property()

# DateTime = DATETIME(
#     storage_format="%(day)02d-%(month)03s-%(year)04d",
#     regexp=r"(\d+)-(\w+)-(\d+)"
# )

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column (String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zipcode = Column(String(15), nullable = True)
    sex = Column(String(1), nullable = True)
    occupation = Column(String(64), nullable = True)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable = False)
    released_at = Column(DATETIME, nullable = True)
    imdb_url = Column(String(128), nullable = True)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable = True)

    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))

def createTable():
    Base.metadata.create_all(ENGINE)

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
