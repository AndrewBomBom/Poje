from flask import Flask, render_template, redirect, request
from data import db_session
from datetime import timedelta, datetime
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import re


from forms.RegForm import RegForm
from forms.LogForm import LogForm
from forms.DeleteForm import Detele_event
from forms.AddEventForm import add_eventForm
from forms.ConfirmUser import ConfirmUser

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
    return redirect('/login')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/starosta_lab', methods=['GET', 'POST'])
@login_required
def starosta_lab():
    form = ConfirmUser()
    db_sess = db_session.create_session()
    starosta_group = str(db_sess.query(User.group_num).filter(User.id == current_user.get_id()).first())
    starosta_group = int(re.sub("[^A-Za-z0-9а-яА-Я ]", "", starosta_group))
    This_group_users = db_sess.query(User).filter(User.group_num == starosta_group, User.confirmed == 0).all()
    confirmed_ids = []
    if request.method == 'POST':
        confirmed_ids = request.form.getlist('checkbox')
        if confirmed_ids == []:
            return render_template('index.html', message = 'Все завяки приняты')
    
    for ids in confirmed_ids:
        last_elem = ids[-1]
        db_sess.query(User).filter(User.id == ids).update({'confirmed' : 1})
        db_sess.commit()
        if ids == last_elem:
            return render_template('index.html', message = "Студенты успешно подтвержены")

        
    return render_template('starosta_lab.html', This_group_users = This_group_users, form = form )



@app.route('/delete_event', methods=['GET', 'POST'])
@login_required
def detele_event():
    db_sess = db_session.create_session()
    form = Detele_event()
    if form.validate_on_submit():
    
        events_this_day = db_sess.query(Event).filter(Event.day_event == form.search_date.data).all()
        
        if events_this_day == []:

            return render_template("DeteteEvent.html", form = form, message = 'В этот день нет событий')
        else:
    

            return render_template("DeteteEvent.html", form = form, data = form.search_date.data, events = events_this_day)
       
    if request.form.getlist('checkbox'):

        for event_id in request.form.getlist('checkbox'):
            event = db_sess.query(Event).filter(Event.id_event == event_id).first()
            db_sess.delete(event)
        db_sess.commit()
        return redirect('/event_table')
    return render_template("DeteteEvent.html", form = form)


    

@app.route('/event_table', methods=['GET', 'POST'])
@login_required
def event_table(): 
    db_sess = db_session.create_session()
    if (re.sub("[^A-Za-z0-9а-яА-Я ]", "", str(db_sess.query(User.confirmed).filter(User.id == current_user.get_id() != True).first())) != 'True' ):
        return render_template('index.html', message = 'Дождитесь подверждения от старосты')
    today_day = datetime.now().date()
    dates = []
    dict_events_today = {}
    for single_date in (today_day + timedelta(n) for n in range(7)):
        dates.append(str(single_date.strftime("%d/%m/%y")))
        user_group = str(db_sess.query(User.group_num).filter(User.id == current_user.get_id()).first())
        user_group = int( re.sub("[^A-Za-z0-9а-яА-Я ]", "", user_group))
        events_today = str(db_sess.query(Event.content).filter(Event.day_event == single_date, Event.writer_group == user_group).all())
        events_today = re.sub("[^A-Za-z0-9а-яА-Я ]", "", events_today)
        dict_events_today[str(single_date.strftime("%d/%m/%y"))] = str(events_today) 
    return render_template('Maintable.html', dates = dates, events_today = dict_events_today)
    
    
    



@app.route('/add_event', methods = ['GET', 'POST'])
@login_required
def add_event():
    db_sess = db_session.create_session()
    if (re.sub("[^A-Za-z0-9а-яА-Я ]", "", str(db_sess.query(User.confirmed).filter(User.id == current_user.get_id() != True).first())) != 'True' ):
        return render_template('index.html', message = 'Дождитесь подверждения от старосты')
    form = add_eventForm()
    if form.validate_on_submit():
        event = Event(
            type_event = form.type_event.data,
            day_event = form.day_event.data,
            time_event = form.time_event.data,
            content = form.content.data,
            writer_group =  re.sub("[^A-Za-z0-9а-яА-Я ]", "", (str(db_sess.query(User.group_num).filter(User.id == current_user.get_id()).first())))
        )

        
        db_sess.add(event)
        db_sess.commit()
        db_sess.close()

        return redirect('/event_table')
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
        for starosta in (db_sess.query(User.Starosta).filter(User.group_num == form.group_num.data).all()):
            if form.Starosta.data == 1:
                print(type(db_sess.query(User.Starosta).filter(User.group_num == form.group_num.data).all()))
                if starosta:
                    return render_template('RegForm.html', message = 'У этой группы есть староста, обратитесь в поддержку', form = form)

        user = User(
             email = form.email.data,
             name = form.name.data,
             lastname = form.lastname.data,
             group_num = form.group_num.data,
             podgroup_num = form.podgroup_num.data,
             Starosta = form.Starosta.data,
             confirmed = False
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
