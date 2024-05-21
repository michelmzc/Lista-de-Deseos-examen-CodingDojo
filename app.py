
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .forms import SignupForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/exam'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = "auth"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/', methods=['GET'])
def auth(register_form=None, login_form=None):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if register_form == None:
        register_form = SignupForm()
    
    if login_form == None:    
        login_form = LoginForm()
        
    return render_template('auth.html', register_form=register_form, login_form=login_form)

@app.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name  = form.name.data 
        email = form.email.data
        password = form.password.data
        user = User.get_by_email(email)
        if user is not None:
            error = f'Email { email } already registed'
            flash(error)
            return redirect(url_for('auth'))
        else:
            flash(f'Register requested for user { form.email.data }')
            user = User(name=name, email=email)
            user.set_password(password)            
            user.save()
            login_user(user)
            return redirect(url_for('index'))
    else: 
        flash('Invalid data in form')        
        return auth(register_form=form)
        
    
    
@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user { form.email.data }')
        user = User.get_by_email(form.email.data)
        if user is not None:                        
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('wrong password') 
                return redirect(url_for('auth'))
        else:
            flash('Invalid user')
            return redirect(url_for('auth'))
    else: 
        flash('Invalid user and password commbination')
        return redirect(url_for('auth'))

@app.route('/logout')
def logout():
    logout_user()
    flash('logged out')
    return redirect(url_for('auth'))

@app.route('/index')
@login_required
def index():
    return render_template('index.html')
