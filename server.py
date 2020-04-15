import os
from flask import Flask, render_template, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import date, timedelta
from dotenv import load_dotenv
from wtforms import Form, IntegerField, TextAreaField, validators

load_dotenv('.env.dev', override=True)

# Check if there is a database url provided by Heroku
# If not, piece the database url together using local credentials
DB_URL = os.getenv("DATABASE_URL", None)
if not DB_URL:
    DB_URL = os.getenv("DEV_POSTGRES_URL")

app = Flask(__name__)
app.secret_key = 'lovebirds'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

preferred_pronouns = { "Andy" : "him", "Sachi" : "her"}
person_image = {"Andy" : "andy.jpg", "Sachi" : "sachi.jpg"}

from models import Rating

class RatingForm(Form):
    attitude_score = IntegerField('Attitude', [validators.NumberRange(min=0, max=10)])
    cleanliness_score = IntegerField('Cleanliness', [validators.NumberRange(min=0, max=10)])
    taste_score = IntegerField('Taste', [validators.NumberRange(min=0, max=10)])
    comment = TextAreaField('Comment', [validators.Length(max=1000)])

@app.route('/', methods = ['GET', 'POST'])
def home():
    form = RatingForm(request.form)
    if request.method == 'POST' and form.validate():
        db.session.add(Rating(subject=get_other_person()[0],
                              day=get_yesterday(),
                              attitude_score=form.attitude_score.data, 
                              cleanliness_score=form.cleanliness_score.data, 
                              taste_score=form.taste_score.data, 
                              comment=form.comment.data))
        db.session.commit()
        flash('Thanks for helping us improve!')
        return redirect(url_for('home'))
    person, pronoun, image_url = get_person()
    other_person, other_pronoun = get_other_person()
    return render_template('home.html', name=person, other_name=other_person, form=form, other_pronoun=other_pronoun, image=image_url)

def get_even():
    today = date.today()
    print("abcdef today is: " + str(today))
    reference_day = date(2020, 3, 28)
    delta = today - reference_day
    print("abcdef delta is: " + str(delta))
    even = delta.days % 2 == 0
    return even

def get_pronoun(person):
    return preferred_pronouns[person]

def get_image(person):
    return person_image[person]

def get_person():
    even = get_even()
    person = "Andy" if even else "Sachi"
    return (person, get_pronoun(person), get_image(person))

def get_other_person():
    even = get_even()
    other_person = "Sachi" if even else "Andy"
    return (other_person, get_pronoun(other_person))

def get_yesterday():
    today = date.today()
    yesterday = today - timedelta(days=1)
    return yesterday

@app.route('/rating')
def rating():
    results = Rating.query.all()
    averages = db.session.query(Rating.subject, func.avg(Rating.attitude_score), func.avg(Rating.cleanliness_score), func.avg(Rating.taste_score), func.avg(Rating.day_average)).group_by(Rating.subject).all()
    print(averages)
    return render_template('rating.html', results=results, averages=averages)





