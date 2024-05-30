from flask_wtf import FlaskForm
from wtforms import SubmitField,DateField
from wtforms.validators import DataRequired

class Detele_event(FlaskForm):
    search_date = DateField('Выберите день',validators=[DataRequired()])
    submit = SubmitField('Поиск')