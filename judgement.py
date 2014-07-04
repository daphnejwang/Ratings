from flask import Flask, render_template, redirect, request, flash, url_for, session
import jinja2
import model
from model import User, Movie, Rating

app = Flask(__name__)
app.secret_key = "topsecretkey"
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    user_list = model.dbsession.query(model.User).join(model.Rating).order_by(model.User.id).limit(5).all()
    return render_template("user_list.html", users=user_list)

@app.route("/movies_list/<int:user_id>")
def list_movies_and_ratings(user_id):
    ratings_list = model.dbsession.query(model.Rating).filter_by(user_id=user_id).all()
    # movies = []
    # for rating in ratings_list:
    #     movie = model.dbsession.query(model.Movie).filter_by(rating.movie_id).all()
    #     movies.append(movie)
    return render_template("movies_list.html", ratings=ratings_list, user_id=user_id)

@app.route("/movies/<int:movie_id>", methods=["GET"])
def movie_page(movie_id):
    print "NAME", movie_id
    movie_details = model.dbsession.query(model.Rating).filter_by(movie_id=movie_id).filter_by(user_id=session['user']).one()
    print movie_details
    return render_template("movies.html", item=movie_details)

@app.route("/movies/<int:movie_id>", methods=["POST"])
def post_rating(movie_id):
    movie_rating = Rating(user_id=session['user'], movie_id=movie_id, rating=request.form['rating'])
    # print movie_rating
    #     # user = User(email=request.form['email'], password= request.form['password'], age=request.form['age'], sex=request.form['sex'], occupation=request.form['occupation'], zipcode=request.form['zipcode'])
    model.dbsession.add(movie_rating)
    model.dbsession.commit()
    return "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

@app.route("/login", methods=["GET"])
def get_userlogin():
    error = None
    return render_template("login.html", error = error)

@app.route("/login", methods=["POST"])
def login_user():
    # print "*************************************"
    # check if user exists in database
    found_user = model.dbsession.query(User).filter_by(email=request.form['email']).first()
    print "found user", found_user
    error = None
    if found_user:
        print "User found"
        session['user'] = found_user.id
        return redirect("/")
    else:
        print "User not found"
        #flash('Invalid username/password.')
        error = "Invalid Username"
        return render_template('login.html', error = error)
    # return redirect("/")

@app.route("/create_newuser", methods=["GET"])
def get_newuser():
    return render_template("newuser.html")

@app.route("/create_newuser", methods=["POST"])
def create_newuser():
    # print "SESSION", model.dbsession
    user_exists = model.dbsession.query(User).filter_by(email=request.form['email']).first()
    print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    print "USER EXISTS", user_exists
    if user_exists != None:
        flash(" User already exists. Please login")
        return redirect("/create_newuser")
    else:     
        user = User(email=request.form['email'], password= request.form['password'], age=request.form['age'], sex=request.form['sex'], occupation=request.form['occupation'], zipcode=request.form['zipcode'])
        model.dbsession.add(user)
        model.dbsession.commit()
        flash("Successfully added new user!")
        return redirect("/")


if __name__ == "__main__":
    app.run(debug = True)