# 9.4.3
from flask import Flask

# create a new Flask instance "app"
app = Flask(__name__)

# define the starting point, also known as the root.
@app.route('/')

def hello_world():
    return 'Hello world'