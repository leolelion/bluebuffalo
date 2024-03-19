from flask import Flask, redirect, render_template, request, flash, url_for, Blueprint
from DashboardProject.analysis import perform_analysis
auth = Blueprint('auth', __name__)


@auth.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@auth.route('/header')
def header():
    return render_template("header.html")

@auth.route('/index')
def index():
    return render_template("index.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/newAccount')
def newAccount():
    return render_template("newAccount.html")

@auth.route('/accountSetting')
def accountSetting():
    return render_template("accountSetting.html")

@auth.route('/map')
def map():
    return render_template("map.html")

# @auth.route('/analysis')
# def analysis():
#     return render_template('analysis.html')

@auth.route('/analysis.py', methods=['GET', 'POST'])
def call_compare():
    result = perform_analysis()
    return result

@auth.route('/test')
def test():
    return render_template('test.html')