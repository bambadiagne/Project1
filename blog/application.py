import os
import requests
from flask import Flask, session, render_template, abort
from flask import redirect, url_for, jsonify, flash
from werkzeug.security import check_password_hash

from flask_session import Session
from requestDatabase import *
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database


@app.route("/index")
@app.route("/")
def index():
    number_books = NUMBERS_BOOKS
    return render_template("index.html", number_books=number_books)


@app.route("/signup")
def signup():
    return render_template("static/auth/signup.html")


@app.route("/signup", methods=['POST'])
def signup_post():
    Fname = request.form.get('Fname')
    Lname = request.form.get('Lname')
    email = request.form.get('email')
    passwd = request.form.get('passwd')

    if(research_user_(Fname, Lname, passwd, email).rowcount == 0):

        insert_user(Fname, Lname, passwd, email)

        return redirect(url_for('login'))

    elif(request_user_signup(Fname, Lname).rowcount >= 1):

        flash('Username  already exists')

        return redirect(url_for("signup"))

    elif (request_email_exists(email) >= 1):

        flash('Email  already exists')
        return redirect(url_for("signup"))


@app.route("/api/<isbn>")
def api(isbn):
    response = result_search_isbn(isbn)
    return jsonify(title=response[2], author=response[3], year=response[4], isbn=response[1])


@app.route("/profile/<isbn>")
def bookpage(isbn):
    book_search = result_search_isbn(isbn)
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "QazefzgsN4PkPaDDVz24Q", "isbns": isbn})
    reviews_goodreads = res.json()
    return render_template('account/bookpage.html', book_search=book_search, reviews_goodreads=reviews_goodreads)


@app.route("/result")
def result():

    return render_template('account/result.html')


@app.route("/profile")
def profile():
    if('user_id' in session):

        pagination_books=pagination(1,ALL_BOOKS,'profile')

        return render_template("account/profile.html", request_user=research_user_id(session['user_id'][0]),pagination=pagination_books)

    return redirect(url_for('login'))


@app.route("/profile", methods=['POST'])
def login_search():
    search = request.form.get('research')
    result_search = pagination(2,list(result_search_book(search,12,2 )),'profile')
    
    if len(result_search[0]) >= 1:
        return render_template('account/result.html', pagination=result_search) 
    else:
        result_search = SUGGESTED_BOOKS
        return render_template('errors/book_not_found.html', result_search_1=result_search)


@app.route('/login')
def login():
    return render_template("static/auth/login.html")


@app.route("/login", methods=['POST'])
def login_post():
    username = request.form.get("username")
    passwd = request.form.get('passwd')
    research_user = request_user(username).fetchone()
    db.commit()
    
    if(not research_user or not check_password_hash(research_user.passwd, passwd)):
        
        flash('Please check your login details and try again.')
    
        return redirect(url_for('login'))
    
    session["user_id"] = []
    session["user_id"].append(research_user[0])
    return redirect(url_for('profile'))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
