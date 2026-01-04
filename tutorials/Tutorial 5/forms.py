from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.widgets import TextArea

from wtforms import StringField, FloatField, TextAreaField, DateField
from models import db, Crop, Field

from datetime import datetime, date, timezone


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
