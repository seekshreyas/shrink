#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Shrinkdb
=========

DB script for Shrink app ::
An app to generate short urls for long urls

python_version = "Python 2.7.5 :: Anaconda 1.6.1 (x86_64)"
"""

import flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = flask.Flask(__name__)
# dburl = 'sqlite:////tmp/shrinklocal.db'
dburl = 'sqlite:////tmp/shrinklocal2.db'

# dburl = 'postgres://rfgihzmnveahtg:UqRf3jksouzSu5XYyQpTPZ-HyX@ec2-54-225-101-199.compute-1.amazonaws.com:5432/d6l97mheia499m'
# dburl = 'postgresql://localhost/shrinklocal'
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
        response = {
            'longurl': self.longurl,
            'shorturl': self.shorturl,
            'hitcount' : self.hitcount
        }

        return json.dumps(response)
        # return response


class Bundles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bundlename = db.Column(db.String(50))

    bundle_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    bundle = db.relationship('Links', backref=db.backref('links', lazy='dynamic'))


    def __init__(self, bundlename):
        self.bundlename = bundlename

    def __repr__(self):

        return json.dumps(self.bundlename)




if __name__ == '__main__':
    db.create_all()
    # pr = Bundle('profile')
    # re = Links('www.github.com/seekshreyas', 'gh', pr)


    # db.session.add(re)
    # db.session.add(pr)




    # db.session.commit()
    # links = Links.query.all()
    # print links


#     # referece: http://stackoverflow.com/questions/17642366/integrity-error-flask-sqlalchemy
    app.run(debug=True, use_reloader=False)



