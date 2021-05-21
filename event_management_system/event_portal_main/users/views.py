from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from event_portal_main import db
from werkzeug.security import generate_password_hash,check_password_hash
from event_portal_main.users.forms import RegistrationForm, LoginForm
from event_portal_main.models import User



users = Blueprint("users",__name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    '''

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
    '''

    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmpassword')

        if password == confirm_password:
            user = User(email = email , username = username , password = password)
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering! Now you can login!')
            return redirect(url_for('users.login'))
        elif password != confirm_password:
            flash("Passwords should match")

    return render_template('register.html')

@users.route('/login', methods=['GET', 'POST'])
def login():
    '''
    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

    '''
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("Username or password is incorrect")

        elif user.check_password(password) and user is not None:
            #Log in the user

            login_user(user)
            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.home')

            return redirect(next)
    return render_template('login.html')


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))
