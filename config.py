from datetime import timedelta
import os
class Config(object):
    SESSION_PERMANENT=True if(os.getenv("SESSION_PERMANENT")=="True") else False
    SESSION_TYPE = os.getenv("SESSION_TYPE")
    PERMANENT_SESSION_LIFETIME= timedelta(hours=24*7)
    SESSION_PERMANENT=bool(os.getenv("SESSION_PERMANENT"))
    SQLALCHEMY_TRACK_MODIFICATIONS=bool(os.getenv("SESSION_PERMANENT"))
    FLASK_APP="blog/app.py"
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY=os.getenv('SECRET_KEY')
    APP_SETTINGS=os.getenv('APP_SETTINGS')
    
