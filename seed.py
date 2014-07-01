import model
from model import User, Movie, Rating
import csv
from datetime import datetime

def load_users(session):
    # use u.user

    with open('seed_data/u.user', 'rb') as csvfile:
        userdata = csv.reader(csvfile, delimiter = "|")
        for row in userdata:
            user = User(id=row[0], age=row[1], sex=row[2], occupation=row[3], zipcode=row[4])
            s.add(user)
        s.commit()
        

def load_movies(session):

    with open('seed_data/u.item', 'rb') as csvfile:
        itemdata = csv.reader(csvfile, delimiter = "|")
        for row in itemdata:
            if row[2] == "":
                py_date = None
            else: 
                py_date = datetime.strptime(row[2], "%d-%b-%Y")
            title = row[1]
            title = title.decode("latin-1")
            movie = Movie(id=row[0], name=title, released_at=py_date, imdb_url=row[4])
            s.add(movie)
            s.commit()


def load_ratings(session):
    # use u.data
    count = 0
    with open('seed_data/u.data', 'rb') as csvfile:
        ratingdata = csv.reader(csvfile, delimiter = "\t")
        for row in ratingdata:
            count += 1
            mrating = Rating(id=count, user_id=row[0], movie_id=row[1], rating=row[2])
            s.add(mrating)
        s.commit()

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    pass

if __name__ == "__main__":
    s= model.connect()
    main(s)

