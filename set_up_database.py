from __future__ import unicode_literals
from main import app
from main import db, User


# Create all the tables
db.create_all()

# Dummy user.

# new_moderator = Moderator(username='hubert_burda', password='theboss')
# new_user = User(username='dummy', email='dummy@dummy.com')

new_user = User(username='Daniil Pakhomov', email='warmspringwinds@gmail.com', password='123', )
# new_user_2 = User(username='Moritz Schworer', email='mr.mosch@gmail.com')
# new_user_3 = User(username='Inci Torcuk', email='inci.torcuk@gmail.com')
# new_user_4 = User(username='Corinna List', email='list.corinna@googlemail.com')
# new_user_5 = User(username='Gerrit Holz', email='mail@gerritholz.com')
 
# new_quiz = Quiz(quiz_question="How do you feel today?")

# db.session.add(new_moderator)
db.session.add(new_user)
# db.session.add(new_user_1)
# db.session.add(new_user_2)
# db.session.add(new_user_3)
# db.session.add(new_user_4)
# db.session.add(new_user_5)

# db.session.add(new_quiz)
db.session.commit()

first_user = User.query.first()
# first_quiz = Quiz.query.first()

# first_quiz = first_quiz.__dict__
# first_user = first_user.__dict__

print first_user.username

# test_reply_url = get_secure_reply_url(first_quiz, first_user)

# print test_reply_url