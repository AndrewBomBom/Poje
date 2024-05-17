from flask_wtf import FlaskForm
from wtforms import SubmitField

class Detele_event(FlaskForm):
    submit = SubmitField('Поиск')