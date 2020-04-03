from flask import Flask, render_template
from datetime import date

app = Flask(__name__)

@app.route('/')
def home():
	today = date.today()
	reference_day = date(2020, 3, 28)
	delta = today - reference_day
	even = delta.days % 2 == 0
	person = "Andy" if even else "Sachi"
	return render_template('home.html', name=person)


@app.route('/template')
def template():
	return render_template('home.html', name='afdjkladsfds')

@app.route('/test')
def test():
    return "this is the test route"