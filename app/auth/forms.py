from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..models import User

class login_Form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me', default=True)
    submit = SubmitField('Login')

class register_Form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1,64)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('conf_password', message='Password must match')])
    conf_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')