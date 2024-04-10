from flask import render_template, request, Blueprint, redirect, url_for
from DashboardProject.analysis import perform_analysis, get_latitude, get_longitude, get_mean_values, get_total_mean, \
    get_prediction
from DashboardProject.dashboard import get_top10_data, get_least10_data, get_pollutant_data, get_aqi_population
from DashboardProject.map import perform_map
from DashboardProject.insertComment import insert_comment
from DashboardProject.displayIndexComment import display_comment_index
from DashboardProject.login import check_login
from flask_login import current_user
from werkzeug.security import generate_password_hash
from DashboardProject.message import email_alert
from . import db
from .models import User, Comment


auth = Blueprint('auth', __name__)


@auth.route('/')
def hello_world():  # put application's code here
    """"""
    return 'Hello World!'


@auth.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user_date = request.args.get('date', '2020-01-01')
    top_cities = get_top10_data(user_date)
    least_cities = get_least10_data(user_date)
    pollutant = get_pollutant_data(user_date)
    aqi_population = get_aqi_population(user_date)
    comment = display_comment_index(user_date)
    return render_template('index.html', top_cities=top_cities, least_cities=least_cities, \
                           aqi_population=aqi_population, pollutant=pollutant, \
                           user_date=user_date, comments=comment)


@auth.route('/header')
def header():
    return render_template("header.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    result = check_login()
    return result


@auth.route('/newAccount')
def newAccount():
    return render_template("newAccount.html")


@auth.route('/accountSetting', methods=['GET', 'POST'])
def accountSetting():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('curremail')
        password = request.form.get('currpass')
        newpass = request.form.get('newpass')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            user.firstName = firstname
            user.lastName = lastname
            if newpass:
                user.password = generate_password_hash(newpass, method='sha256')
            db.session.commit()
            return redirect(url_for('auth.accountSetting'))
    return render_template("accountSetting.html")


@auth.route('/map', methods=['GET', 'POST'])
def map():
    result = perform_map()
    return result


@auth.route('/map_test')
def map_test():
    return render_template('map_test.html')


@auth.route('/latitude', methods=['GET', 'POST'])
def latitude():
    city = request.form.get('city')
    latitude = get_latitude(city)
    return latitude


@auth.route('/longitude', methods=['GET', 'POST'])
def longitude():
    city = request.form.get('city')
    longitude = get_longitude(city)
    return longitude


@auth.route('/analysisMean', methods=['GET', 'POST'])
def analysis_mean():
    city = request.form.get('city')
    mean = get_mean_values(city)
    return mean


@auth.route('/analysisTotal', methods=['GET', 'POST'])
def analysis_total():
    city = request.form.get('city')
    total = get_total_mean(city)
    return total


@auth.route('/analysisPrediction', methods=['GET', 'POST'])
def analysis_prediction():
    city = request.form.get('city')
    data = get_total_mean(city)
    prediction = get_prediction(data)
    prediction_list = prediction.tolist()
    return prediction_list


@auth.route('/testMessage', methods=['GET', 'POST'])
def testMessage():
    recipient = request.form.get('email')
    result = email_alert("Account Confirmation",
                         "Thank you for creating an account! We're happy to have you here! Enjoy learning about Air Quality!",
                         recipient)
    return redirect(url_for('auth.dashboard'))


@auth.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')


@auth.route('/insertComment', methods=['GET', 'POST'])
def insertComment_analysis():
    type, result = insert_comment()
    if type == "analysis":
        return redirect(url_for('auth.analysis', city=result))
    else:
        return redirect(url_for('auth.dashboard', date=result))


@auth.route('/analysis', methods=['GET', 'POST'])
def analysis():
    cityName = request.args.get('city')
    result = perform_analysis(cityName)
    return result

@auth.route('/delete_comment', methods=['POST'])
def delete_comment():
    comment_id = request.form.get('commentId')
    comment = Comment.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('auth.dashboard'))