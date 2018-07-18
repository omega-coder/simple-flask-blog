from flask import render_template, url_for, redirect, flash
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog import app
from flask_blog.models import User, Post

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Account created for {}!".format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Logged in successfully', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login Portal', form=form)


