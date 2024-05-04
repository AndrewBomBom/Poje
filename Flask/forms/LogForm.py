from flask_wtf import FlaskForm
from wtforms import EmailField,StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired

class LogForm(FlaskForm):
    email = EmailField('Почта',validators=[DataRequired()])
    password = PasswordField('Пароль',validators=[DataRequired()])
    submit = SubmitField('Войти')
