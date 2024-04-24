from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('base.html')

@app.route('/login')
def window():
    return render_template('loginform.html')


app.run(debug='True')
