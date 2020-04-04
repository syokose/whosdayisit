import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from dotenv import load_dotenv

load_dotenv('.env.dev')

POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PW = os.getenv("POSTGRES_PW")
POSTGRES_DB = os.getenv("POSTGRES_DB")

app = Flask(__name__)

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, unique=False, nullable=False)
    day = db.Column(db.Date, nullable=False)
    attitude_score = db.Column(db.Integer)
    cleanliness_score = db.Column(db.Integer)
    taste_score = db.Column(db.Integer)

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

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')