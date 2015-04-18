import flask
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView, helpers
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__, static_folder='./public/', static_url_path='')

app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/dan/University/projects/hackathon/database.db'

db = SQLAlchemy(app)

admin = Admin(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    github_url = db.Column(db.String(120))

    def __init__(self, username="", email="", password="", github_url=""):
        self.username = username
        self.email = email
        self.password = password
        self.github_url = github_url
        
    def __repr__(self):
        return '<User %r>' % self.username
        
admin.add_view(ModelView(User, db.session))

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')