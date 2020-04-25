import os
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask import Flask, session , render_template,abort
from flask import redirect,request,url_for,jsonify,flash 
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import login_required,current_user
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
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/index")
@app.route("/")
def index():
    number_books = db.execute("SELECT COUNT(*) FROM books").fetchone()
    return render_template("index.html",number_books=number_books)

@app.route("/signup")
def signup():
   return render_template("static/auth/signup.html")

@app.route("/signup",methods=['POST'])
def signup_post():
    Fname = request.form.get('Fname')
    Lname = request.form.get('Lname')
    email = request.form.get('email')
    passwd = request.form.get('passwd')
     
    if(db.execute("SELECT *FROM users where username = :username or email= :email", {"username": Fname+" "+Lname,"email": email}).rowcount == 0):
        db.execute("INSERT INTO users (username,passwd,email) VALUES (:username,:passwd,:email)",{'username':Fname+' '+Lname,"passwd":generate_password_hash(passwd, method='sha256'),'email':email})       
        db.commit()
        return redirect(url_for('login'))
    elif(db.execute("SELECT *FROM users where username = :username ", {"username": Fname+" "+Lname}).rowcount>=1):

        flash('Username  already exists')
        return redirect(url_for("signup"))
    elif (db.execute("SELECT *FROM users where  email= :email", {"email": email}).rowcount>=1):

        flash('Email  already exists')    
        return redirect(url_for("signup"))


@app.route("/api/<isbn>")
def api(isbn):
    response =db.execute("SELECT *FROM BOOKS WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
    
    return jsonify(title=response[2],author=response[3],year=response[4],isbn=response[1])

@app.route("/profile/<isbn>")
def bookpage(isbn):
    book_search=db.execute("SELECT *FROM BOOKS WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "QazefzgsN4PkPaDDVz24Q", "isbns": isbn})
    reviews_goodreads=res.json()
    return render_template('account/bookpage.html',book_search=book_search,reviews_goodreads=reviews_goodreads)

@app.route("/result")
def result():
    
    return render_template('account/result.html')


@app.route("/profile")
def profile():
    request_user=db.execute("SELECT *FROM USERS WHERE id_user= :id",{"id":session["user_id"][0]}).fetchone()
    return render_template("account/profile.html",request_user=request_user)

@app.route("/profile",methods=['POST'])
def login_search():
    search = request.form.get('research')
    result_search = db.execute("SELECT *FROM BOOKS WHERE isbn LIKE :search or title_book LIKE :search or author_book LIKE :search",{"search":'%'+search+'%'}).fetchall()    
    if len(result_search) >= 1:
        return render_template('account/result.html',result_search=result_search)
    else :
        result_search=db.execute("SELECT *FROM BOOKS ORDER BY RANDOM() LIMIT 4").fetchall()
        return render_template('errors/book_not_found.html',result_search=result_search)


@app.route('/login')
def login():   
   return render_template("static/auth/login.html")

@app.route("/login",methods=['POST'])
def login_post():
    username=request.form.get("username")   
    passwd=request.form.get('passwd')
    request_user=db.execute('SELECT *FROM users where username = :username ',{"username":username,}).fetchone()
    db.commit()
    
    if(not request_user or not check_password_hash(request_user.passwd, passwd)):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
    session["user_id"]=[]
    session["user_id"].append(request_user[0])
    return redirect(url_for('profile'))#.html',request_user=request_user)
     
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
