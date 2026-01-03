# Tutoril 4 - Databases

In this tutorial we will cover the design and implementation of a database using DB Browser and Python's SQLAlchemy library.

## Creating a New Database

In DB Browser, click on `New Database` and create a new database called `database.db` in the root directory of the project. Then, click on `Execute SQL` and run the following command:

```SQL
CREATE TABLE "Crops" (
    "ID"            TEXT NOT NULL UNIQUE,
    "Name"          TEXT NOT NULL,
    "Sowing"        TEXT NOT NULL,
    "TargetYield"   REAL NOT NULL,
    "Value"         REAL NOT NULL,
    PRIMARY KEY("ID") 
);
```

What this does is create a table in which we can put data about the crops we might like to grow. How this works will be explained in the in-person class, but in simple terms, we create a table called crops with several fields which are either text, or reals (numbers with decimals), and a primary key called *ID* which uniquely identifies each row in the table. None of these columns may be empty for any record.

We can now create a more complex table to hold information about our fields, called `Fields` using this code:

```SQL
CREATE TABLE "Fields" (
	"ID"	        TEXT NOT NULL UNIQUE,
	"Area"	        REAL NOT NULL,
	"Crop"	        TEXT NOT NULL,
	"Name"	        TEXT NOT NULL UNIQUE,
	"Created"	    TEXT NOT NULL,
	"Irrigation"	TEXT NOT NULL DEFAULT 'Rainfed',
	"Drainage"	    TEXT NOT NULL DEFAULT 'Medium',
	"Risk"	        TEXT NOT NULL DEFAULT 'Moderate',
	"pH"	        REAL NOT NULL DEFAULT 7.0,
	"SOM"	        REAL NOT NULL,
	"SoilType"	    TEXT NOT NULL,
	"Notes"	        TEXT,
	"SowingDate"	TEXT,
	PRIMARY KEY("ID"),
	FOREIGN KEY("Crop") REFERENCES "Crops"("ID") ON DELETE CASCADE
);
```

This code does the same, with extra columns, but here, some of the fields are not marked as `NOT NULL` which means that they are allowed to contain no data. We also set some defaults for some columns which are the values inserted automatically if none is provided by the user or programmer.

We also define a *foreign key* which references our `Crops` table by the ID of that crop. This means we can be sure we are referencing a crop which is defined in that table, and avoids creating one massive table with duplicated data containing data both for crops and fields.

## Inserting Records into the Database

Inserting records into a database is fairly simple, and we can add some example data into both tables by running the SQL code in `example_data.sql`. The syntax for doing so follows the format `INSERT INTO <table name> (<columns>) VALUES (<values>)`.

## Getting Records from the Database

We will not cover the syntax for SQL queries which retrieve data from a database here, but you may want to familiarize yourself with the syntax and also with joins on [W3Schools' SQL tutorials](https://www.w3schools.com/sql/).

Flask, however, provides a simpler way to interact with the database by providing an Object Reference Manager (ORM), which is what we will be using.

### Configuring and Connecting to the Database

Once you have inserted the example records into the database, we can create a connection to the database in a new file in the root directory called `models.py` by writing the following:

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime, timezone


db = SQLAlchemy()
db_name = 'database.db'
```

Before running this code, you should `pip install` the following packages (datetime comes preinstalled):
 - sqlalchemy
 - flask_sqlalchemy

This creates an instance of `SQLAlchemy` which we can use to connect to the database and defines the name of the file our database is stored in.

Now we can add `from models import db, db_name` to the top of `main.py` to get access to the variables we just defined, and then add the following configuration settings for the database just under where we define the variable `app = Flask(__name__)`, what these do will be covered in the in-person class:

```python
# Resolve an absolute path to the SQLite database in the same directory as this file.
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "database.db")

# Flask / SQLAlchemy configuration.
# NOTE: SQLALCHEMY_TRACK_MODIFICATIONS is usually set to False to avoid overhead,
# but it's left as-is here to match the existing application behavior.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Used by Flask-WTF to protect forms against CSRF; change for production.
app.config["SECRET_KEY"] = "dev-secret-change-me"

# Bind SQLAlchemy to the Flask app.
db.init_app(app)
```

### Representing Our Data in Code

We can now add some classes to our `models.py` file which will represent the structure of the tables we created earlier and then also import these in `main.py` and then move on to providing them in the pages we have created. The code for the models is in `models.py` in this folder, and you should be familiar by now with how to import these models into `main.py`.

The code for how we can retrieve the data from Fields and then display it in our main route is:

```python
@app.route('/')
def main():
    # Query all fields that have an associated crop (inner join),
    # ordered alphabetically by field name.
    fields = (
        db.session.execute(
            db.select(Field)
            .join(Field.crop_rel)
            .order_by(Field.name)
        )
        .scalars()
        .all()
    )

    # Build template context for the dashboard.
    context = {
        "title": "Home",
        "fields": fields
    }

    return render_template('main.html', context=context)
```

This query selects all the data from the Field table, joins it to the Crop table, and orders it by the name of the field and then returns all the resulting records. This is then passed to the context dictionary. This is approximately equivalent to this SQL query:

```SQL
SELECT * FROM Fields JOIN Crops ON Fields.Crop=Crops.ID;
```

### Displaying it in the Webpage

We will begin by modifying our homepage to display all the fields in the table we created rather than showing dummy data. We can do this by replacing the body of the table with the following:

```HTML
{% for field in context.fields %}
  <tr>
    <td>{{ field.name }}</td>
    <td>{{ field.area | round(2) }} ha</td>
    <td>{{ field.crop_rel.name }}</td>
    <td>
      <a href="{{ url_for('field_view', field_id=field.id) }}" class="btn btn-primary btn-sm">View</a>
      <a href="#" class="btn btn-danger btn-sm">Delete</a>
    </td>
  </tr>
{% endfor %}
```

This iterates through each element in the fields we passed to the template and displays that field's data in the table. It also creates a link to that page's details page, which we will now sort out.

We can also adapt our code for the field details view to get the data from the field we are looking at and display it on the page. The code would look something like this:

```python
@app.route('/field/<field_id>')
def field_view(field_id):
    field_data = Field.query.get(field_id)
    context = {
        "title": field_data.name,
        "field": field_data
    }

    return render_template('view.html', context=context)
```

If we are getting just one record from a table by its primary key (in this case *ID*), this is so common that Flask provides a special function for doing so: `<Model>.query.get(<id>)`.

The code in file `view.html` in this folder shows how the code for this page should look. Note how we display data with double curly brackets like `{{ context.field.name }}` and we will see how we can use common programming constructs like for and if statements with curly brackets like this:

```
{% if context.field.name == "Unknown" %}
    <html here>
{% else %}
    <html here>
{% endif %}

{% for item in context.items %}
    <html here>
{% endfor %}
```

This allows us to create semi-complex structures and logic within our frontend code.

This will be covered in more depth in the in-person class.

## Advanced: Designing a Database With the 3rd Normal Form (3NF)

When we are designing a database, we follow certain principles to make the data in the database easy to access, work with, ensure its consistency, and to reduce duplication, which are all goals which support one another. To do this, we design databases to adhere to the rules of *normal forms*. This tutorial will concern itself with the 1st, 2nd, and 3rd normal form.

### 1st Normal Form

For a table in a database to be in the 1st normal form (1NF), it must follow these rules:
 - The data must be *atomic*, meaning each cell must contain only 1 single, indivisible value, so no lists of values or subtables are permitted, and
 - There may be no repeated columns or data, and
 - Each row must be unique and not a duplicate of another, and
 - Each row must be uniquely identified by a *primary key*

As previously stated, a *primary key* is a column/attribute which is unique to that record and will never, under any circumstances, be duplicated. This is often a number or semi-structured random string allocated when the record is created such as `A964E53F` or `7764` or `C-5963`. It is better for security for the primary key of a table to be unpredictable and hard to guess, so usually you should not use email addresses or names as a primary key.

A primary key may be a *composite key* made up of 2 or more columns where neither column is unique on its own, but together they are always unique. 2nd Normal Form will show why these types of primary keys are best avoided.

### 2nd Normal Form

For a table to be in 2nd Normal Form (2NF), it must be:
 - In the 1st normal form, and,
 - Have no partial dependencies

A *partial dependency* is when the value of a column depends on only part of the primary key if it is a composite primary key, so you could tell what the value of a column is without knowing the full primary key. 

A table is automatically in 2NF if it is in 1NF and its primary key is not composite (consists of only 1 column).

## 3rd Normal Form

For a table to be in 3rd Normal Form (3NF), it must be:
 - In the 2nd normal form, and,
 - Have no transitive dependencies

This means that you must not be able to tell what the value of a column is based on any other attribute except the primary key. In other words:

<p style="font-size: 1.5em;">The value of a column must depend on the primary key, the whole primary key, and nothing but the primary key!</p>

There are more levels of normal forms, going up to the 6th normal form, but 3NF is sufficient for most applications.

## Conclusion

In conclusion, we have now looked at how to create and work with a database using both SQL code and using Flask's ORM. We have also looked at how to use Flask's templating engine Jinja2 to display this data on our pages.

In the next tutorial we will look at creating some forms for the user to be able to create their own fields, and also to create a diary of operations which have been performed on the fields.
