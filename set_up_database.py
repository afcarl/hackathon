from __future__ import unicode_literals
from main import app
from main import db, User, ProjectProposal


db.drop_all()
db.create_all()


new_user = User(username='Daniil Pakhomov', email='warmspringwinds@gmail.com',
                password='123', github_url='hh')

new_project = ProjectProposal(name="facebook clone", description="create a facebook clone",
                            tags_string="python datascience", author=new_user)


db.session.add(new_user)
db.session.add(new_project)

db.session.commit()

first_user = User.query.first()

print first_user.username
