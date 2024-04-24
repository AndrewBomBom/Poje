from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired


class RegForm(FlaskForm):
    name = StringField('Имя',validators=[DataRequired()])
    # lastname = StringField('Фамилия', validators=[DataRequired()])
    # group_num = StringField('Номер группы', validators=[DataRequired()])
    # podgroup_num = StringField('Номер подруппы')
    # Starosta = BooleanField('Вы староста этой группы?')
    # password = PasswordField('Пароль')
    # password_rep = PasswordField('Повторите пароль',validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')