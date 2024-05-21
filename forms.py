from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):    
    name     = StringField('Name', validators=[DataRequired()])
    #alias    = StringField('Alias', validators=[DataRequired()])    
    email    = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message="Password must be equals.")])
    password_confirm = PasswordField('Confirm PW', validators=[DataRequired()])
    #birth     = DateField('Date of Birth')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):    
    email    = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])    
    submit   = SubmitField('Login')

class QuoteForm(FlaskForm):    
    id      = IntegerField('id')
    user_id = IntegerField('id')
    author  = StringField('Author', validators=[DataRequired(), Length(min=2)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])    
    submit  = SubmitField('Submit')    