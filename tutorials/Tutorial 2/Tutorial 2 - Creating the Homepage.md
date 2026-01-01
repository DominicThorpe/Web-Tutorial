# Tutorial 2 - Creating the Homepage

We will now consider how to make a simple homepage which, for now, will just show static, preprogrammed data.

## Some Important Definitions

 - HTML (Hypertext Markup Language): this code is usually contained in files ending in `.html` and they tell the browser what should be on the webpage, such as text, buttons, forms, and tables
 - CSS (Cascading StyleSheet): this can be inside an HTML file, or contained in its own file, usually ending in `.css`. This is useless on its own, but paired with HTML, it tells the browser how the HTML elements should look, such as size, colour, simple animations, and more
 - JS (JavaScript): also can be in an HTML file or in a standalone `.js` file. This tells the browser how things should behave, such as what to do when a button is clicked, or when data needs to be loaded from an external source like another webpage
 - Bootstrap: a CSS framework which provides a lot of CSS styling straight out the box so we can write less code ourselves
 - Responsivity: today, 70% of web traffic is from mobile devices and tablets, and yet we develop on laptops and desktops! Responsivity is how we change the layout of the webpage depending on the size of the screen being used to make it useable on devices of all sizes. Bootstrap is a very useful tool for creating responsive layouts.

## Creating the Base

All the pages we create will have a common header and import the same CSS and JS libraries, so to avoid writing the same code over and over, Flask's templating engine Jinja allows us to write the shared code once in its own file and then reference that quickly on each page. The code we will be using for this base is in this folder in *base.html*, and the CSS styling is in *style.css*.

In the same directory as where you put `main.py`, create two folders called `templates` and `static`, and put *base.html* in templates and *style.css* in static, so that Flask knows where to find them.

The elements of these files will be covered in the in-person class.

## Creating the Homepage

The code for the homepage should also go in the *templates* folder and be called `main.html`. The code for this page can be found in this folder and is called *main.html*.

How this file works will be explained in the in-person class, but it is worth noting that for now we are using dummy values - these will be replaced when we create the database and some data to go in it.

## Creating the Flask Route

In your project's directory, create a file called `main.py` and put the following code:

```python
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def main():
    context = {"title": "Home"}
    return render_template('main.html', context=context)
```

This loads the Flask library, creates a Flask web server to serve our files to the browser, creates a route the user can navigate to, and then tells the web server what page to send to the user's browser.

<h5>The file *main.html* ***must*** be in the folder *templates* or Flask will not be able to find it</h5>.

## Conclusion

In conclusion, we have created a simple webpage to display some simple data about some fields. In the next tutorial we will work on creating a page which can give significantly more data on a field and cover how to work with APIs provided by external entities.
