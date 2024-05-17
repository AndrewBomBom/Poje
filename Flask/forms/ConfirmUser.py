from flask_wtf import FlaskForm
from wtforms import BooleanField,SubmitField
from wtforms.validators import DataRequired

class ConfirmUser(FlaskForm):
    confirm_user = BooleanField('Есть такой студент в вашей группе?')
    submit = SubmitField('Обновить базу данных', validators=[DataRequired()])