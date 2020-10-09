import sys,os

sys.path.append(os.getcwd()+'/blog')
from app import app

if __name__ == "__main__":
    app.run()