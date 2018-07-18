from flask import Flask, render_template, url_for, redirect, session, flash, request
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# Random Secret

app.config['SECRET_KEY'] = '2d1d36485bb9ce3d1982d45094d9fe04'


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
    return render_template('login.html', title='Login Portal', form=form)


if __name__ == "__main__":
    app.run(debug=True)
