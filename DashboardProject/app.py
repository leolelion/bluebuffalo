from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/header')
def header():
    return render_template("header.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/newAccount')
def newAccount():
    return render_template("newAccount.html")

@app.route('/accountSetting')
def accountSetting():
    return render_template("accountSetting.html")

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/analysis')
def analysis():
    return render_template("analysis.html")



if __name__ == '__main__':
    app.run()