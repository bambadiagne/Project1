import sys,os
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.append(os.getcwd()+'/blog')
print(sys.path)
from app import app

if __name__ == "__main__":
    app.run()