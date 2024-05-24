from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):    
    name     = StringField('Name', validators=[DataRequired(), Length(min=3)])
    #alias    = StringField('Alias', validators=[DataRequired()])    
    email    = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message="Password must be equals.")])
    password_confirm = PasswordField('Confirm PW', validators=[DataRequired()])
    date_hired = DateField('Date Hired')
    submit = SubmitField('Register')


class LoginForm(FlaskForm):    
    email    = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])    
    submit   = SubmitField('Login')

class ItemForm(FlaskForm):    
    name      = StringField('Item/Product', validators=[DataRequired(), Length(min=3)])
    submit    = SubmitField('Add')    