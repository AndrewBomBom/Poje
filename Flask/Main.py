from flask import Flask, render_template, redirect, abort
from Forms_py.RegForm import RegForm



app = Flask(__name__)
app.config['SECRET_KEY'] = 'digitalDepartment'


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')

@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegForm()
    print(form.errors)
    print(form.name.data)
    if form.validate_on_submit():
        return redirect('/index')
        
    return render_template('RegForm.html', title = 'Регистрация', form = form)


def main():
    app.run(debug=True)
    



if __name__ == '__main__':
    main()
