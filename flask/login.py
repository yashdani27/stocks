from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class LoginForm(FlaskForm):
    company = StringField('Search for a company...')
    search = SubmitField('Search')