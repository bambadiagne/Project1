import os
from werkzeug.security import generate_password_hash, check_password_hash
#import requests
from flask import Flask, session , render_template,abort
from flask import redirect,request,url_for 
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def signup():
   return render_template("static/auth/signup.html")

@app.route("/signup",methods=['POST'])
def signup_post():
    Fname = request.form.get('Fname')
    Lname = request.form.get('Lname')
    email = request.form.get('email')
    passwd = request.form.get('passwd')
     
    if(db.execute("SELECT *FROM users where username = :username", {"username": Fname+" "+Lname}).rowcount == 0):
        db.execute("INSERT INTO users (username,passwd,email) VALUES (:username,:passwd,:email)",{'username':Fname+' '+Lname,"passwd":generate_password_hash(passwd, method='sha256'),'email':email})       
        db.commit()
        return redirect(url_for('login'))
    else:
        #flash('Username already exists')
        return redirect(url_for("signup"))

@app.route("/profile")
def profile():
    return "account/profile.html"

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
        return redirect(url_for('login'))
    return render_template('account/profile.html',request_user = request_user)
     
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
