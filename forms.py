from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
    SelectField
)

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp ,Optional
import email_validator
from flask_login import current_user
from wtforms import ValidationError,validators
from models import User




class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])
    # Placeholder labels to enable form rendering
    username = StringField(
        validators=[Optional()]
    )

class profile_form(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(1, 64)])
    lastname = StringField(validators=[InputRequired(), Length(1, 64)])
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    address = StringField(validators=[InputRequired(), Length(1, 64)])
    address2 = StringField(validators=[InputRequired(), Length(1, 64)])
    city = StringField(validators=[InputRequired(), Length(1, 64)])
    state = StringField(validators=[InputRequired(), Length(1, 64)])
    zip = StringField(validators=[InputRequired(), Length(1, 64)])
    



class register_form(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("pwd", message="Passwords must match !"),
        ]
    )
    token = StringField(validators=[InputRequired(), Length(1, 20)])

class vote_form(FlaskForm):
    voted = SelectField('Select a norminee')







    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_uname(self, uname):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")