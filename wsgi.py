import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(0, 'C:/Users/user/important/Projet EDX/project1/blog')

from app import app

if __name__ == "__main__":
    app.run()