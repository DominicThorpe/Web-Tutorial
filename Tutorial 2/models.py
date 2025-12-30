from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


db = SQLAlchemy()
db_name = 'database.db'


class Crop(db.Model):
    __tablename__ = "Crops"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sowing = db.Column(db.String)
    targetYield = db.Column(db.Float)

    fields = db.relationship("Field", back_populates="crop_rel")


class Field(db.Model):
    __tablename__ = "Fields"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    area = db.Column(db.Float)

    # Foreign key column (this is the key missing piece)
    crop = db.Column(db.String, db.ForeignKey("Crops.id"), nullable=True)

    # Relationship (this gives you field.crop)
    crop_rel = db.relationship("Crop", back_populates="fields")

