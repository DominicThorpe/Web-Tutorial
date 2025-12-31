from flask import Flask
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from wtforms_sqlalchemy.fields import QuerySelectField
from statistics import mode
import os, random

from models import db, db_name, Field, Crop


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

    context = {
        "title": "Home", 
        "fields": fields,
        "total_area": sum([field.area for field in fields]),
        "main_crop": mode([field.crop_rel.name for field in fields])
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
    print(field_id)
    Field.query.filter_by(id = field_id).delete()
    db.session.commit()

    return redirect("/")
