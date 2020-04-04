from flask import Flask, render_template
from datetime import date

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(debug=True, host='0.0.0.0')

@app.route('/')
def home():
	today = date.today()
	reference_day = date(2020, 3, 28)
	delta = today - reference_day
	even = delta.days % 2 == 0
	person = "Andy" if even else "Sachi"
	other_person = "Sachi" if even else "Andy"
	return render_template('home.html', name=person, other_name=other_person)



@app.route('/template')
def template():
	return render_template('home.html', name='afdjkladsfds')

@app.route('/test')
def test():
    return "this is the test route"