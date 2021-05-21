# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# User Based Imports
from flask_login import current_user
from event_portal_main.models import User

class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired() , Email()],render_kw={"placeholder":"Email"})
    password  = PasswordField(validators=[DataRequired()],render_kw={"placeholder":"Password"})
    submit = SubmitField("Log in")

class RegistrationForm(FlaskForm):
    email = StringField(validators=[DataRequired(),Email()],render_kw={"placeholder":"Email"})
    username = StringField(validators=[DataRequired()],render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')],render_kw={"placeholder":"Enter Password"})
    pass_confirm = PasswordField(validators=[DataRequired()],render_kw={"placeholder":"Confirm Password"})
    submit = SubmitField('Register!')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')

