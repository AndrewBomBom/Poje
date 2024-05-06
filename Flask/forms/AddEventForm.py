from flask_wtf import FlaskForm
from wtforms import DateField, TextAreaField, DateTimeField, SelectField, SubmitField, TimeField
from wtforms.validators import DataRequired

class add_eventForm(FlaskForm):
    event_types = ['Перенос пары', 'Праздник', 'Экзамен','Зачет']
     
    type_event = SelectField('Тип события', choices=event_types, validate_choice=[DataRequired()])
    day_event = DateField('День события', validators=[DataRequired()])
    time_event = TimeField('Время события', validators=[DataRequired()])
    content = TextAreaField('Событие', validators=[DataRequired()])
    submit = SubmitField('Добавить')
