from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import UserPassword
from enum import Enum

# enum for email validation errors
class EmailError(Enum):
    INVALID_EMAIL_DOMAIN = "Please use a gator email address"
    EMAIL_IN_DB = "You already have an account. Please log in."
    VALID_EMAIL = "Valid email"


class SignupForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()], render_kw={"placeholder": "First name", "class": "login-item", "id": "firstName"})
    last_name = StringField('Last name', validators=[DataRequired()], render_kw={"placeholder": "Last name", "class": "login-item", "id": "lastName"})
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email", "class": "login-item", "id": "email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "login-item", "id": "password"})

    submit = SubmitField('Sign-Up')


    def validate_email(self, email):
        #check if email is already in database
        user = UserPassword.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(EmailError.EMAIL_IN_DB.value)
        
        #check if email is already in ends in uhd.edu
        if not email.data.endswith('gator.uhd.edu') and not email.data.endswith('uhd.edu'):
            raise ValidationError(EmailError.INVALID_EMAIL_DOMAIN.value)
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "Login Email", "class": "login-item"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "login-item"})
    submit = SubmitField('Log in')

    def __repr__(self):
        return '<User {}>'.format(self.email)





