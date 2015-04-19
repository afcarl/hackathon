import flask
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView, helpers
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import form, fields, validators
from flask import render_template, request, url_for, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from elasticsearch import Elasticsearch
import datetime



app = flask.Flask(__name__, static_folder='./public/', static_url_path='')

app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/dan/University/projects/hackathon/database.db'

es_hadler = Elasticsearch()

db = SQLAlchemy(app)

admin = Admin(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    github_url = db.Column(db.String(120))
    
    # Projects array that the user created.
    # The property in ProjectProposal objects will be named author.
    projects = db.relationship("ProjectProposal", backref="author")
    
    def __init__(self, username="", email="", password="", github_url=""):
        self.username = username
        self.email = email
        self.password = password
        self.github_url = github_url
    
    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
    
    def __repr__(self):
        return '<User %r>' % self.username

class ProjectProposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))
    tags_string = db.Column(db.String(120))
    quiz_date = db.Column(db.DateTime)
    
    # You can access the user who created it through the 'author' property.
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, author, name="", description="", tags_string="", date=None):
        if date is None:
            date = datetime.datetime.utcnow()
        self.date = date
        self.name = name
        self.description = description
        self.tags_string = tags_string
        self.author = author
        
    def __repr__(self):
        return '<User %r>' % self.username

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    username = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_username(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()

admin.add_view(ModelView(User, db.session))

exclude_user = ['projects']
exclude_project = ['author', 'author_id']

user_form = model_form(User, Form, exclude=exclude_user)
project_form = model_form(ProjectProposal, Form, exclude=exclude_project)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.route('/')
def index():
    return render_template('main_view.html')

@app.route('/search')
def search():
    return render_template('search_view.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard_view.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # login and validate the user...
        user = form.get_user()
        login_user(user)
        flash("Logged in successfully.")
        return redirect(url_for("search"))
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/user/<int:user_id>")
def user_view(user_id):
    
    user = User.query.get_or_404(user_id)
    
    return render_template('user_view.html', user=user)

@app.route("/project/<int:project_id>")
def project_view(project_id):
    
    project = ProjectProposal.query.get_or_404(project_id)
    
    return render_template('project_view.html', project=project)

@app.route("/user", methods=['GET', 'POST'])
def user_register():
    
    form = user_form(request.form)
    if request.method == 'POST':
        user = User(form.username.data, form.email.data,
                    form.password.data, form.github_url.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        login_user(user)
        return redirect(url_for('user_view', user_id=user.id))
    
    return render_template('user_register_view.html', form=form)

@app.route("/project",  methods=['GET', 'POST'])
@login_required
def project_create():
    
    form = project_form(request.form)
    if request.method == 'POST':
        project = ProjectProposal(current_user, form.name.data,
                   form.description.data, form.tags_string.data)
        db.session.add(project)
        db.session.commit()
        flash('The project proposal has been created')
        return redirect(url_for('project_view', project_id=project.id))
    
    return render_template('project_create_view.html', form=form)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')