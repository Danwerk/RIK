from app import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    registry_code = db.Column(db.String(7), unique=True, nullable=False)
    established_date = db.Column(db.Date, nullable=False)
    total_capital = db.Column(db.Integer, nullable=False)
    shareholders = db.relationship("Shareholder", backref="company", lazy=True)

class Shareholder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    company_name = db.Column(db.String(100))
    personal_code = db.Column(db.String(11))
    registry_code = db.Column(db.String(7))
    share = db.Column(db.Integer, nullable=False)
    is_founder = db.Column(db.Boolean, default=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)