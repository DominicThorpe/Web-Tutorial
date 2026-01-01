"""
Flask application entrypoint for a simple farm/field management app.

This module:
- Configures the Flask app and SQLAlchemy connection (SQLite).
- Provides routes to view a dashboard, view/edit fields, and create/delete operations.
- Uses WTForms (Flask-WTF) for Field and Operation creation/editing.

Templates expected:
- main.html
- view.html
- new_field.html
- new_operation.html
"""

from flask import Flask
from flask import render_template, redirect
from statistics import mode
import os, random

from forms import FieldForm, OperationForm
from models import db, db_name, Field, Crop, Operation


app = Flask(__name__)

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


@app.route('/')
def main():
    """
    Render the home/dashboard page.
    """
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

    # Aggregate totals by crop name across all fields.
    # Structure:
    # crop_totals = {
    #   "Wheat": {"area": 12.5, "yield": 8.0, "value": 180.0},
    #   ...
    # }
    crop_totals = {}
    for field in fields:
        # First time we see this crop name, initialise its summary.
        if field.crop_rel.name not in crop_totals.keys():
            crop_totals[field.crop_rel.name] = {
                "area": field.area,
                "yield": field.crop_rel.targetYield,
                "value": field.crop_rel.value
            }
        else:
            # Otherwise, increment area under that crop.
            crop_totals[field.crop_rel.name]['area'] += field.area

    # Build template context for the dashboard.
    context = {
        "title": "Home",
        "fields": fields,

        # Total area across all listed fields.
        "total_area": sum([field.area for field in fields]),

        # Total estimated value across all fields based on crop economics.
        "total_value": sum([field.area * field.crop_rel.value * field.crop_rel.targetYield for field in fields]),

        # Most common crop across the fields (raises if list is empty).
        "main_crop": mode([field.crop_rel.name for field in fields]),

        # Per-crop aggregated totals for dashboard display.
        "crop_totals": crop_totals
    }

    return render_template('main.html', context=context)


@app.route('/field/<field_id>')
def field_view(field_id):
    """
    Render a detail page for a single field.

    Args:
        field_id (str): Primary key of the Field to display.
    """
    field_data = Field.query.get(field_id)
    context = {
        "title": field_data.name,
        "field": field_data
    }

    return render_template('view.html', context=context)


def gen_field_id():
    """
    Generate a simple human-readable ID for a Field.

    Returns:
        str: An ID of the form 'C-####' (e.g. 'C-0042').

    Notes:
        - Uses random numbers, so collisions are possible.
        - If uniqueness matters, consider checking the database or using UUIDs.
    """
    return f"C-{random.randrange(0, 9999):04d}"


@app.route("/field/new", methods=["GET", "POST"])
def field_new():
    """
    Create a new Field.

    GET:
        Render a blank FieldForm.

    POST:
        Validate the submitted form and create a new Field record.

    Returns:
        - On success: Redirect to the home page.
        - On failure or GET: Render new_field.html with the form.
    """
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


@app.route("/field/edit/<field_id>", methods=["GET", "POST"])
def field_edit(field_id):
    """
    Edit an existing Field.

    Args:
        field_id (str): Primary key of the Field to edit.

    GET:
        Render FieldForm pre-populated with the Field's current values.

    POST:
        Validate and save the updated values back to the database.

    Returns:
        - On success: Redirect to the field detail page.
        - On failure or GET: Render new_field.html with the form.
    """
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


@app.route("/field/delete/<field_id>", methods=["GET"])
def field_delete(field_id):
    """
    Delete a Field by ID.

    Args:
        field_id (str): Primary key of the Field to delete.

    Returns:
        Redirect to the home page.

    Notes:
        This uses a GET request for deletion, which is convenient but not ideal:
        destructive actions are typically done via POST/DELETE to reduce accidental deletes.
    """
    Field.query.filter_by(id=field_id).delete()
    db.session.commit()

    return redirect("/")


def gen_operation_id():
    """
    Generate a simple human-readable ID for an Operation.

    Returns:
        str: An ID of the form 'OP-########' (e.g. 'OP-00001234').

    Notes:
        - Uses random numbers, so collisions are possible.
        - Consider UUIDs or a database-generated primary key for robustness.
    """
    return f"OP-{random.randrange(0, 99999999):08d}"


@app.route("/operation/new/<field_id>", methods=["GET", "POST"])
def operation_new(field_id):
    """
    Create a new Operation linked to a specific Field.

    Args:
        field_id (str): Primary key of the Field to attach the operation to.

    GET:
        Render an OperationForm with the field pre-selected.

    POST:
        Validate the submitted form and create an Operation record.

    Returns:
        - On success: Redirect to the field detail page.
        - On failure or GET: Render new_operation.html with the form and field.
    """
    form = OperationForm()

    # Pre-select the Field relationship in the form so the user doesn't need to choose it.
    form.field_rel.data = Field.query.get(field_id)

    if form.validate_on_submit():
        operation = Operation()
        form.populate_obj(operation)
        operation.id = gen_operation_id()

        db.session.add(operation)
        db.session.commit()

        return redirect(f"/field/{field_id}")

    context = {
        "title": "New Operation",
        "form": form,
        "field": Field.query.get(field_id)
    }

    return render_template("new_operation.html", context=context)


@app.route("/operation/delete/<operation_id>", methods=["GET"])
def operation_delete(operation_id):
    """
    Delete an Operation by ID.

    Args:
        operation_id (str): Primary key of the Operation to delete.

    Returns:
        Redirect to the associated field detail page.

    Notes:
        This performs deletion via GET which is not ideal for destructive actions.
    """
    # Capture the associated field ID before deleting so we can redirect back.
    field_id = Operation.query.get(operation_id).field

    Operation.query.filter_by(id=operation_id).delete()
    db.session.commit()

    return redirect(f"/field/{field_id}")
