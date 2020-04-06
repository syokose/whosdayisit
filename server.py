import os
from flask import Flask, render_template, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
from dotenv import load_dotenv
from wtforms import Form, IntegerField, TextAreaField, validators

load_dotenv('.env.dev')

POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PW = os.getenv("POSTGRES_PW")
POSTGRES_DB = os.getenv("POSTGRES_DB")

app = Flask(__name__)
app.secret_key = 'lovebirds'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

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
    comment = db.Column(db.String)

    def __repr__(self):
        return 'Rating(subect='+self.subject+', day='+str(self.day)+ ')'

class RatingForm(Form):
    attitude_score = IntegerField('Attitude', [validators.NumberRange(min=0, max=10)])
    cleanliness_score = IntegerField('Cleanliness', [validators.NumberRange(min=0, max=10)])
    taste_score = IntegerField('Taste', [validators.NumberRange(min=0, max=10)])
    comment = TextAreaField('Comment', [validators.Length(max=1000)])

@app.route('/', methods = ['GET', 'POST'])
def home():
    form = RatingForm(request.form)
    if request.method == 'POST' and form.validate():
        db.session.add(Rating(subject=get_other_person(),
                              day=get_yesterday(),
                              attitude_score=form.attitude_score.data, 
                              cleanliness_score=form.cleanliness_score.data, 
                              taste_score=form.taste_score.data, 
                              comment=form.comment.data))
        db.session.commit()
        flash('Thanks for helping us improve!')
        return redirect(url_for('home'))
    person = get_person()
    other_person = get_other_person()
    return render_template('home.html', name=person, other_name=other_person, form=form)

def get_even():
    today = date.today()
    reference_day = date(2020, 3, 28)
    delta = today - reference_day
    even = delta.days % 2 == 0
    return even

def get_person():
    even = get_even()
    person = "Andy" if even else "Sachi"
    return person

def get_other_person():
    even = get_even()
    other_person = "Sachi" if even else "Andy"
    return other_person

def get_yesterday():
    today = date.today()
    yesterday = today - timedelta(days=1)
    return yesterday

@app.route('/', methods=['POST'])
def handle_data():
    print("form submit")
    attitude_score = request.form['attitude_score']
    cleanliness_score = request.form['cleanliness_score']
    taste_score = request.form['taste_score']
    comment=request.form['comment']
    print(attitude_score, cleanliness_score, taste_score, comment)
    db.session.add(Rating(subject=get_other_person(), day=get_yesterday(),attitude_score=attitude_score, cleanliness_score=cleanliness_score, taste_score=taste_score, comment=comment))
    db.session.commit()
    return home()

@app.route('/test_read')
def test_read():
    result = str(Rating.query.all())
    return result







