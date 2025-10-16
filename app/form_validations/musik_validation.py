from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField)
from wtforms.validators import InputRequired, Length

class MusikValidation(FlaskForm):
    judul = StringField("Judul",validators=[InputRequired()])
    penyanyi = StringField("penyanyi",validators=[InputRequired()])
    genre = StringField("genre",validators=[InputRequired()])