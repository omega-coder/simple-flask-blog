import sqlalchemy
from flask import render_template, url_for, redirect, flash, request
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog import app, db, bcrypt
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
posts = [
    {
        'author': 'omega_coder',
        'title': 'Blog post 1',
        'content': 'Blog post 1 content',
        'date_posted': '15 Jul, 2018'
    },
    {
        'author': 'omega_coder',
        'title': 'Blog post 2',
        'content': 'Blog post 2 content',
        'date_posted': '16 Jul, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    title = 'About'
    return render_template('about.html', title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_field.data)
            next_page = request.args.get('next')
            flash('Logged in successfully', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Wrong Email/Password combination!', 'danger')
    return render_template('login.html', title='Login Portal', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out!', 'info')
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')