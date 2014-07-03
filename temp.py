user = session.query(model.User).get(35)
ratings = session.query(model.Rating).filter_by(user_id=user.id).all()
movies = []
for r in ratings:
    movie = session.query(model.Movie).get(r.movie_id)
    movies.append(movie)

for m in movies:
    print m.title