from flask import Flask, render_template, redirect, request, flash, url_for, session
import jinja2
import model
from model import User, Movie, Rating

app = Flask(__name__)
app.secret_key = "topsecretkey"
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    user_list = model.dbsession.query(model.User).limit(5).all()
    return render_template("user_list.html", users=user_list)

@app.route("/login", methods=["GET"])
def get_userlogin():
    error = None
    return render_template("login.html", error = error)

@app.route("/login", methods=["POST"])
def login_user():
    print "*************************************"
    # check if user exists in database
    found_user = model.dbsession.query(User).filter_by(email=request.form['email']).all()
    print "found user", found_user
    error = None
    if found_user:
        print "User found"
        session['user'] = found_user.id
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
    user = User(email=request.form['email'], password= request.form['password'], age=request.form['age'], sex=request.form['sex'], occupation=request.form['occupation'], zipcode=request.form['zipcode'])
    model.dbsession.add(user)
    model.dbsession.commit()

    flash("Successfully added new user!")
    return redirect("/")

# @app.route("/login", methods=["GET"])
# def show_login():
#     if "username" in session:
#         message = "%s is logged in." % session['username']
#         return render_template("logout.html", message=message)
#     return render_template("login.html")


# @app.route("/login", methods=["POST"])
# def process_login():
#     """TODO: Receive the user's login credentials located in the 'request.form'
#     dictionary, look up the user, and store them in the session.
#     test email: ashley@eimbee.biz, frances@jabbercube.org
#     """
#     error = None
#     email = request.form['email']
#     customer = model.get_customer_by_email(email)
#     if customer:
#         session['username'] = customer.first_name
#         return redirect("/melons")
#     else:
#         error = 'Invalid username/password.'
#     return render_template('login.html', error = error)

if __name__ == "__main__":
    app.run(debug = True)