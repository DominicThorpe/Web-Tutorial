from flask import Flask
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, DateField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from wtforms_sqlalchemy.fields import QuerySelectField
from statistics import mode
from datetime import datetime, date, timezone
import os, random

from models import db, db_name, Field, Crop, Operation


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "database.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SECRET_KEY"] = "dev-secret-change-me"

db.init_app(app)


class CropForm(FlaskForm):
    class Meta:
        model = Crop


class FieldForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    pH = FloatField('pH', validators=[DataRequired()])
    area = FloatField('Area', validators=[DataRequired()])
    SOM = FloatField('Soil Organic Matter', validators=[DataRequired()])
    soilType = StringField('Soil Type', validators=[DataRequired()])
    risk = StringField('Risk', validators=[DataRequired()])
    irrigation = StringField('Irrigation', validators=[DataRequired()])
    drainage = StringField('Drainage', validators=[DataRequired()])
    sowingDate = DateField('Sowing Date')
    notes = TextAreaField('Notes', widget=TextArea())

    crop_rel = QuerySelectField(
        "Current Crop",
        query_factory=lambda: Crop.query.order_by(Crop.name).all(),
        get_label="name",
        allow_blank=True
    )

    created = db.Column(
        db.String,
        nullable=False,
        default=lambda: datetime.now(timezone.utc).isoformat()
    )


class OperationForm(FlaskForm):
    date = DateField("Date", default=date.today, validators=[DataRequired()])
    operation = StringField("Operation", validators=[DataRequired()])
    detail = StringField("Product / Detail")
    rate = StringField("Rate")
    
    field_rel = QuerySelectField(
        "Field",
        query_factory=lambda: Field.query.order_by(Field.name).all(),
        get_label="name",
        allow_blank=False
    )


@app.route('/')
def main():
    fields = (
        db.session.execute(
            db.select(Field)
            .join(Field.crop_rel)
            .order_by(Field.name)
        )
        .scalars()
        .all()
    )

    crop_totals = {}
    for field in fields:
        if field.crop_rel.name not in crop_totals.keys():
            crop_totals[field.crop_rel.name] = {
                "area": field.area,
                "yield": field.crop_rel.targetYield,
                "value": field.crop_rel.value
            }
        else:
            crop_totals[field.crop_rel.name]['area'] += field.area

    context = {
        "title": "Home", 
        "fields": fields,
        "total_area": sum([field.area for field in fields]),
        "total_value": sum([field.area * field.crop_rel.value * field.crop_rel.targetYield for field in fields]),
        "main_crop": mode([field.crop_rel.name for field in fields]),
        "crop_totals": crop_totals
    }

    return render_template('main.html', context=context)


@app.route('/field/<field_id>')
def field_view(field_id):
    field_data = Field.query.get(field_id)
    context = {
        "title": field_data.name,
        "field": field_data
    }

    return render_template('view.html', context=context)


def gen_field_id():
    return f"C-{random.randrange(0, 9999):04d}"


@app.route("/field/new", methods=["GET", "POST"])
def field_new():
    form = FieldForm()
    if form.validate_on_submit():
        field = Field()
        form.populate_obj(field)
        field.id = gen_field_id()

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
    field = Field.query.get(field_id)
    form = FieldForm(obj=field)

    if form.validate_on_submit():
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
    Field.query.filter_by(id = field_id).delete()
    db.session.commit()

    return redirect("/")


def gen_operation_id():
    return f"OP-{random.randrange(0, 99999999):08d}"


@app.route("/operation/new/<field_id>", methods=["GET", "POST"])
def operation_new(field_id):
    form = OperationForm()
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
    field_id = Operation.query.get(operation_id).field

    Operation.query.filter_by(id = operation_id).delete()
    db.session.commit()

    return redirect(f"/field/{field_id}")
