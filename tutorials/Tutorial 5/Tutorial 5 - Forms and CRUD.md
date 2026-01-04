# Tutorial 5 - Forms and CRUD

In this tutorial we will cover how to create some forms which will allow the user to create new fields and edit the info of fields we have already created, and also create a simple "field diary" of what has been done on the field. We will also allow the user to delete operations and fields. This will mean we have a full CRUD app (Create, Read, Update, and Delete).

## Creating Forms

To create forms install the packages `wtforms` and `wtforms_sqlalchemy` using pip. 

Now create a file called `forms.py` and use the content in `forms.py` in this folder. We will go over the content of this file in the in-person class, but for now we will go over:
 - `StringField`, `FloatField`, `DateField`, and `TextField` all represent different kinds of data we will get from our form: numeric, short bits of text, long bits of text, and dates
 - Most of our fields have the `DataRequired()` validator, which means that the form will be rejected if one or more of these fields is empty.
 - `crop_rel` is a dropdown list which contains all the crops in the `Crops` table in alphabetical order. It gets these by querying the `Crops` table for all its records
 - `Created` is a field which has a default, starting value of the time the form is submitted. The user will not see this input on the form, but it will exist in the background so that the server has a value to use for that column in the database.

## Creating a View for Creating Fields

### Displaying the Form

Now we can create a new function in `main.py` which can display our form:

```python
@app.route("/field/new", methods=["GET", "POST"])
def field_new():
    form = FieldForm()
    context = {
        "title": "New Field",
        "form": form
    }

    return render_template('new_field.html', context=context)
```

Of course, we also need to create the `new_field.html` file in the *templates* folder. The content of this file can be found in the `new_field.html` file in this folder. Note that in the form you must include `{{ context.form.csrf_token }}` which provides a signature to the data in the form when it is sent back to the server; this is essential as without it the data will be insecure and Flask will reject it.

Let's look at one of the fields:

```HTML 
<div class="col-md-6">
  <label class="form-label">Name</label>
  {{ context.form.name(class="form-control", placeholder="e.g., North Field") }}
  <div class="form-text">Use a name farmers will recognise quickly.</div>
</div>
```

We use `col-md-6` to say that on a larger screen, like a laptop, this field should only take up half the width of its container, but should take up the full width on a smaller screen like a phone. We include a label so the user knows what the field is for, and reinforce this with a placeholder of an example value. We display the field itself by displaying the pregenerated HTML created by wtforms with `{{ context.form.name(class="form-control", placeholder="e.g., North Field") }}`, and we also give some extra context/advice with an optional subheading.

### Using the Form

Now we will, of course, need to alter the backend so that when we click *Submit*, the form will actually create a new field. We can do this with this code which will be explained in the in-person class:

```python
def gen_field_id():
    return f"F-{random.randrange(0, 9999):04d}"


@app.route("/field/new", methods=["GET", "POST"])
def field_new():
    form = FieldForm()
    if form.validate_on_submit():
        # Create a new ORM object and populate it from form fields.
        field = Field()
        form.populate_obj(field)

        # Assign an application-level identifier.
        field.id = gen_field_id()

        # Persist to the database.
        db.session.add(field)
        db.session.commit()

        return redirect("/")

    context = {
        "title": "New Field",
        "form": form
    }

    return render_template('new_field.html', context=context)
```

You should now be able to fill out the form and submit it, which should create a new field.

## Updating Fields

Updating a field is very similar and we can even use the same form but with a different route which looks like this:

```python
@app.route("/field/edit/<field_id>", methods=["GET", "POST"])
def field_edit(field_id):
    field = Field.query.get(field_id)

    # Bind the form to an existing object so fields pre-populate on GET.
    form = FieldForm(obj=field)

    if form.validate_on_submit():
        # Apply submitted form values to the ORM object.
        form.populate_obj(field)
        db.session.add(field)
        db.session.commit()

        return redirect(f"/field/{field_id}")

    context = {
        'title': f"Edit {field.id}",
        'form': form
    }

    return render_template('new_field.html', context=context)
```

## Deleting Fields

We can now create a route for deleting fields we no longer want, which is made very easy by Flask's ORM:

```python
@app.route("/field/delete/<field_id>", methods=["GET"])
def field_delete(field_id):
    Field.query.filter_by(id=field_id).delete()
    db.session.commit()

    return redirect("/")
```

We can call this from a link like this: `<a href="{{ url_for('field_delete', field_id=field.id) }}" class="btn btn-danger btn-sm">Delete</a>` which will delete the referenced field from the database.

## Your Turn: Creating the Field Diary

For this activity, create a table with the following columns:
 - ID (String, not null)
 - Date (String, not null)
 - Operation (String, not null)
 - Detail (String)
 - Rate (String)
 - Field (Foreign key, not null)

Then create a route which allows the user to go to a page with a form which allows them to add a new operation to a field, and another route which deletes a specific operation, and connect these routes to the field details view page. An example of how this could be done is shown in the completed project files.   
