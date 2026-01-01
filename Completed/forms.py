"""
WTForms definitions for managing agricultural fields and field operations.

This module defines Flask-WTF forms used to create and edit:
- Fields (land parcels with soil, risk, and crop data)
- Operations (management actions applied to fields, such as sowing or spraying)

The forms integrate with SQLAlchemy models via QuerySelectField to allow selection of related 
database objects.
"""

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.widgets import TextArea

from wtforms import StringField, FloatField, TextAreaField, DateField
from models import db, Crop, Field

from datetime import datetime, date, timezone


class FieldForm(FlaskForm):
    """
    Form for creating and editing a Field record.

    This form captures agronomic, soil, and management-related attributes for a field, as well as 
    its current crop association.
    """

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
    """
    Form for recording a management operation carried out on a field.

    Operations represent discrete actions such as planting, fertilising, spraying, harvesting, or 
    other field activities.
    """

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
