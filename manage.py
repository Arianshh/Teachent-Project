#! /usr/bin/env python

from Teachent import app, db
from Teachent.models import Teacher, Student
from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()

    db.session.commit()
    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print('Dropped the database')


if __name__ == '__main__':
    manager.run()
