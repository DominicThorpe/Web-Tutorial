from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime, timezone


db = SQLAlchemy()
db_name = 'database.db'


class Crop(db.Model):
    __tablename__ = "Crops"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sowing = db.Column(db.String)
    targetYield = db.Column(db.Float)
    value = db.Column(db.Float)

    fields = db.relationship("Field", back_populates="crop_rel")


class Field(db.Model):
    __tablename__ = "Fields"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    area = db.Column(db.Float)
    soilType = db.Column(db.String)
    risk = db.Column(db.String)
    irrigation = db.Column(db.String)
    drainage = db.Column(db.String)
    pH = db.Column(db.Float)
    SOM = db.Column(db.Float)
    sowingDate = db.Column(db.String)
    notes = db.Column(db.String)
    created = db.Column(db.String, default=lambda: datetime.now(timezone.utc).isoformat())

    crop = db.Column(db.String, db.ForeignKey("Crops.id"), nullable=True)
    crop_rel = db.relationship("Crop", back_populates="fields")

    operations = db.relationship("Operation", back_populates="field_rel", order_by="Operation.date")


class Operation(db.Model):
    __tablename__ = "Operations"

    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.String, nullable=False, default=lambda: date.today().isoformat())
    operation = db.Column(db.String, nullable=False)
    detail = db.Column(db.String)
    rate = db.Column(db.String)

    field = db.Column(db.String, db.ForeignKey("Fields.id"), nullable=False)

    field_rel = db.relationship("Field", back_populates="operations")
