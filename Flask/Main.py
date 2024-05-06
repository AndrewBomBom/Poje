from flask import Flask, render_template, redirect, abort
from data import db_session
import datetime
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from forms.RegForm import RegForm
from forms.LogForm import LogForm
from forms.AddEventForm import add_eventForm

from data.user_model import User
from data.event_model import Event



app = Flask(__name__)
app.config['SECRET_KEY'] = 'digitalDepartment'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/index')


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')

@app.route('/event_table')
def event_table():
    db_sess = db_session.create_session()
    today_day = datetime.datetime.now().date()
    # today_day = datetime.datetime.strftime(today_day,'%d.%m.%Y')
    dates = []
    for single_date in (today_day + datetime.timedelta(n) for n in range(4)):
        dates.append(single_date)
    return render_template('Maintable.html', dates = dates)
    



@app.route('/add_event', methods = ['GET', 'POST'])
def add_event():
    form = add_eventForm()
    if form.validate_on_submit():
        event = Event(
            type_event = form.type_event.data,
            day_event = form.day_event.data,
            time_event = form.time_event.data,
            content = form.content.data,
            writer_id = current_user.get_id()
        )

        db_sess = db_session.create_session()
        db_sess.add(event)
        db_sess.commit()
        db_sess.close()
        return redirect('/index')
    return render_template('AddEvent.html', title = 'Добавления события', form = form)      

@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        if form.password.data != form.password_rep.data:
                return render_template('RegForm.html', title = 'Регистрация', form = form, message = 'Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('RegForm.html', title = 'Регистрация', form = form, message = 'Пользователь с такой почтой уже существует')

        user = User(
             email = form.email.data,
             name = form.name.data,
             lastname = form.lastname.data,
             group_num = form.group_num.data,
             podgroup_num = form.podgroup_num.data,
             Starosta = form.Starosta.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')
    return render_template('RegForm.html', title = 'Регистрация', form = form)

@app.route('/login', methods = ['GET','POST'])
def login():
    form = LogForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/index')
    return render_template('LogForm.html', title='Вход', form = form)
    


def main():
    db_session.global_init('Flask/db/DataBase.db')
    app.run(debug=True)
    



if __name__ == '__main__':
    main()
