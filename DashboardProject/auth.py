from flask import render_template, request, Blueprint, redirect, url_for
from DashboardProject.analysis import perform_analysis, get_latitude, get_longitude, get_mean_values, get_total_mean, get_prediction
from DashboardProject.dashboard import get_top10_data, get_least10_data, get_pollutant_data, get_aqi_population
from DashboardProject.map import perform_map
from DashboardProject.insertComment import insert_comment
from DashboardProject.displayIndexComment import display_comment_index
from DashboardProject.login import check_login
from DashboardProject.newAccount import check_newAccount

from DashboardProject.message import email_alert

auth = Blueprint('auth', __name__)
@auth.route('/')
def hello_world():  # put application's code here
    """"""
    return 'Hello World!'
@auth.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        user_date = request.form['date']
        top_cities = get_top10_data(user_date)
        least_cities = get_least10_data(user_date)
        pollutant = get_pollutant_data(user_date)
        aqi_population = get_aqi_population(user_date)
        comment = display_comment_index(user_date)
        return render_template('index.html', top_cities=top_cities, \
                               least_cities=least_cities, aqi_population=aqi_population,\
                                  pollutant=pollutant, user_date=user_date, comments=comment)
    else:
        user_date = "2020-01-01"
        top_cities = get_top10_data(user_date)
        least_cities = get_least10_data(user_date)
        pollutant = get_pollutant_data(user_date)
        aqi_population = get_aqi_population(user_date)
        comment = display_comment_index(user_date)
        return render_template('index.html', top_cities=top_cities, least_cities=least_cities,\
                                aqi_population=aqi_population, pollutant=pollutant,\
                                  user_date=user_date, comments=comment)

@auth.route('/header')
def header():
    return render_template("header.html")

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/login', methods=['GET', 'POST'])
def login_post():
    result = check_login()
    return result

@auth.route('/newAccount')
def newAccount():
    return render_template("newAccount.html")

@auth.route('/newAccount', methods=['GET', 'POST'])
def newAccount_post():
    result = check_newAccount()
    return result

@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/accountSetting')
def accountSetting():
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
    result = email_alert("Account Confirmation", "Thank you for creating an account! We're happy to have you here! Enjoy learning about Air Quality!", recipient)
    return redirect(url_for('auth.dashboard'))

@auth.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')

@auth.route('/insertComment', methods=['GET', 'POST'])
def insertComment():
    result = insert_comment()
    return redirect(url_for('auth.dashboard'))

@auth.route('/analysis', methods=['GET', 'POST'])
def analysis():
    cityName = request.form.get('city')
    result = perform_analysis(cityName)
    return result
