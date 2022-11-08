import os
SESSION_PERMANENT=bool(os.getenv("SESSION_PERMANENT"))
SESSION_TYPE = os.getenv("SESSION_TYPE")
SQLALCHEMY_TRACK_MODIFICATIONS=bool(os.getenv("SESSION_PERMANENT"))
FLASK_APP="blog/app.py"
SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL').replace('postgres','postgresql')
