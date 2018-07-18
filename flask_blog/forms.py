from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Sign Up')

    @staticmethod
    def validate_username(username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Username taken, please choose another one')

    @staticmethod
    def validate_email(email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already exists, choose another one')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember_field = BooleanField('Remember me')
    submit = SubmitField('Sign In')