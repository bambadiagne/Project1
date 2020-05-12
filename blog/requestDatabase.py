import os
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import url_for,request



engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#REQUESTS FOR BOOKS

ALL_BOOKS = db.execute("SELECT * FROM books").fetchall()

NUMBERS_BOOKS = len(ALL_BOOKS)

SUGGESTED_BOOKS = db.execute("SELECT *FROM BOOKS ORDER BY RANDOM() LIMIT 4").fetchall()


def result_search_isbn (isbn):

   return db.execute("SELECT *FROM BOOKS WHERE isbn = :isbn",{"isbn":isbn}).fetchone()

def result_search_book(search,limit,offset):   
   
   single_result_isbn=db.execute("SELECT *FROM BOOKS WHERE isbn LIKE :search LIMIT :limit OFFSET :offset  ",{"search":'%'+search+'%',"limit":limit,"offset":offset}).fetchall()    
   
   single_result_title=db.execute("SELECT *FROM BOOKS WHERE title_book LIKE :search LIMIT :limit OFFSET :offset ",{"search":'%'+search+'%',"limit":limit,"offset":offset}).fetchall()    
   
   single_result_author=db.execute("SELECT *FROM BOOKS WHERE author_book LIKE :search LIMIT :limit OFFSET :offset ",{"search":'%'+search+'%',"limit":limit,"offset":offset}).fetchall()    
   
   if(single_result_isbn is not []):
       
       return single_result_isbn
   
   if(single_result_title is not []):
       
       return single_result_title
   
   if(single_result_author is not []):
       
       return single_result_author
   
   return db.execute("SELECT *FROM BOOKS WHERE isbn LIKE :search or title_book LIKE :search or author_book LIKE :search LIMIT :limit OFFSET :offset",{"search":'%'+search+'%',"limit":limit,"offset":offset}).fetchall()    
             
   

#REQUESTS FOR USERS 

def insert_user(Fname,Lname,passwd,email):
   db.execute("INSERT INTO USERS (username,passwd,email) VALUES (:username,:passwd,:email)",{'username':Fname+' '+Lname,"passwd":generate_password_hash(passwd, method='sha256'),'email':email})
   db.commit()            

def research_user(Fname,Lname,passwd,email):
    
    return db.execute("SELECT *FROM USERS where username = :username or email= :email", {"username": Fname+" "+Lname,"email": email})

def research_user_id(id):
    
    return db.execute("SELECT *FROM USERS where id_user = :id_user ", {"id_user":id})



def request_user_signup(Fname,Lname):
    
    return db.execute('SELECT *FROM USERS where username = :username ',{"username":Fname+" "+Lname,})

def request_user(username):
    
    return db.execute('SELECT *FROM USERS where username = :username ',{"username":username,})

def request_email_exists(email):
    
    return db.execute("SELECT *FROM USERS where  email= :email", {"email": email}).rowcount


def pagination(i:int(),length,route,search=""):
         
         per_page = 12 # define how many results you want per page  
         page = request.args.get('page', 1, type=int)
         pages = len(length) // per_page # this is the number of pages
         offset = (page-1)*per_page # offset for SQL query
         limit = 20 if page == pages else per_page # limit for SQL query
         prev_url = url_for(route, page=page-1) if page > 1 else None
         next_url = url_for(route, page=page+1) if page < pages else None
         if(i==1):
         
            result_search = db.execute("SELECT *FROM BOOKS LIMIT :limit OFFSET :offset ",{"limit":limit,"offset":offset}).fetchall()    
            return result_search,prev_url,next_url,page

         elif(i==2):
            result_search=result_search_book(search,limit,offset)   
            return result_search,prev_url,next_url,page



