from flask import Flask
from flask import render_template
from statistics import mode
import os

from models import db, db_name, Field, Crop


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "database.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)


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
