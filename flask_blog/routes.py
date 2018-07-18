import os
from PIL import Image
from flask import render_template, url_for, redirect, flash, request
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_blog import app, db, bcrypt
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import uuid

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


def save_pic(form_picture):
    base_name = str(uuid.uuid4())[-12:]
    _, file_ext = os.path.splitext(form_picture.filename)
    pic = base_name + file_ext
    full_path = os.path.join(app.root_path, 'static/users_profile_pics', pic)

    out_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(out_size)

    i.save(full_path)

    return pic


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_pic(form.picture.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated Successfully', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)
