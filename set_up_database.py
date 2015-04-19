from __future__ import unicode_literals
from main import app
from main import db, User, ProjectProposal
from lib import save_project_and_index, save_user_and_index
from elasticsearch import Elasticsearch
import datetime
import random

import time

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return datetime.datetime.fromtimestamp(ptime)
    #return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)


db.drop_all()
db.create_all()

es_hadler = Elasticsearch()


new_user = User(username='Daniil Pakhomov', email='warmspringwinds@gmail.com',
                password='123', github_url='hh')

save_user_and_index(db, es_hadler, new_user)


languages = ['python', 'php', 'js']

related_tech =  [
                ['flask', 'django', 'pylone', 'pylons', 'datascience'], 
                ['laravel', 'zend', 'ignition', 'stone', 'wordpress', 'drupal'],
                ['reactjs', 'angular', 'ember', 'backbone', 'nodejs', 'cordova']
                ]

for step in xrange(100):
    
    tags = ''
    
    first_choice = random.choice(range(len(languages)))
    tags = tags + languages[first_choice]
    
    second_array = related_tech[first_choice]
    
    second_choice = random.choice(range(len(second_array)))
    tags = tags + ' ' + second_array[second_choice]
    
    random_date = randomDate("3/1/2015 1:30 PM", "4/20/2015 4:50 AM", random.random())
    
    print new_user.__dict__
    
    new_project = ProjectProposal(name="facebook clone", description="create a facebook clone",
                            tags_string=tags, author=new_user, date=random_date)
    
    save_project_and_index(db, es_hadler, new_project)


# db.session.add(new_user)
# db.session.add(new_project)

# db.session.commit()



# first_user = User.query.first()

# print first_user.username
