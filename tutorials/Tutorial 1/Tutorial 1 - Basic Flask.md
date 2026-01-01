# Tutorial 1 - Basic Flask

The goal of this tutorial is to give you a basic ide of how to use Flask and get started with this project.

Find the quickstart for Flask [here](https://flask.palletsprojects.com/en/stable/quickstart/)

## Installation

Start by installing Flask using *pip* which is installed automatically when you install Python by running this command: `pip install flask`. We have to install many such libraries throughout this project, but they will all follow this pattern.

## Creating a Minimal Application

This is how we create a minimal working Flask application:

```python
from flask import Flask // give Python access to the Flask library

app = Flask(__name__) // create a Flask app

// create a route
@app.route("/") 
// define what that route does by returning a simple header 
def main():
    return "<h1>Hello world!</h1>"
```

Now run `python -m flask --app main run --debug` to run the application and go to the stated address and you should see your webpage displayed!
