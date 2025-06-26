from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("welcome.html")

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/users')
def users():
    return render_template("users.html")

@app.route('/devices')
def devices():
    return render_template("devices.html")

@app.route('/countries')
def countries():
    return render_template("countries.html")

if __name__ == '__main__':
    app.run(debug=True)
