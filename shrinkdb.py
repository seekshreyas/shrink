#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
ShrinkDB
=========

DB script for Shrink app ::
An app to generate short urls for long urls


author = "Shreyas"
email = "shreyas@ischool.berkeley.edu"
python_version = "Python 2.7.5 :: Anaconda 1.6.1 (x86_64)"
"""

import flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime


app = flask.Flask(__name__)
dburl = 'postgresql://localhost/shrinklocal'
app.config['SQLALCHEMY_DATABASE_URI'] = dburl

db = SQLAlchemy(app)



class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longurl = db.Column(db.String(120), unique=True)
    shorturl = db.Column(db.String(80), unique=True)
    creationdate = db.Column(db.DateTime)
    hitcount = db.Column(db.Integer)


    def __init__(self, longurl, shorturl, bundle):
        self.longurl = longurl
        self.shorturl = shorturl

        self.hitcount = 1
        self.creationdate = datetime.utcnow()


    def __repr__(self):
        return '<Shorturl %r>' % self.shorturl


class Bundle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bundlename = db.Column(db.String(50))

    bundle_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    bundle = db.relationship('Links', backref=db.backref('links', lazy='joined'))


    def __init__(self, bundlename):
        self.bundlename = bundlename

    def __repr__(self):
        return '<Bundle %r>' % self.bundlename




if __name__ == '__main__':
    db.create_all()
    pr = Bundle('profile-sh')
    re = Links('www.seekshreyas.com', 'sshr', pr)


    db.session.add(re)
    db.session.add(pr)

    links = Links.query.all()


    db.session.commit()
    print links


    # referece: http://stackoverflow.com/questions/17642366/integrity-error-flask-sqlalchemy
    app.run(debug=True, use_reloader=False)



