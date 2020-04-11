from manage import db
from sqlalchemy.orm import column_property

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, unique=False, nullable=False)
    day = db.Column(db.Date, nullable=False)
    attitude_score = db.Column(db.Integer)
    cleanliness_score = db.Column(db.Integer)
    taste_score = db.Column(db.Integer)
    day_average = column_property((attitude_score + cleanliness_score + taste_score)/3)
    comment = db.Column(db.String)

    def __repr__(self):
        return 'Rating(subject='+self.subject+', day='+str(self.day)+ ')'