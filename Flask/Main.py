from flask import Flask, render_template, redirect, abort
from data import db_session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from forms.RegForm import RegForm
from forms.LogForm import LogForm

from data.user_model import User



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
    print(form.validate_on_submit())
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            return redirect('/index')
    return render_template('LogForm.html', title='Вход', form = form)
    


def main():
    db_session.global_init('Flask/db/DataBase.db')
    app.run(debug=True)
    



if __name__ == '__main__':
    main()
