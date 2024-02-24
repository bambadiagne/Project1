import sys,os

sys.path.append(os.getcwd()+'/blog')
from app import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ['FLASK_RUN_PORT'], debug=os.environ['FLASK_DEBUG'])
