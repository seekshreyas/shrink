#!/usr/bin/env python

import shelve
import flask
from flask import request
# from os import environ
from shrinkdb import db
from shrinkdb import Links
from shrinkdb import Bundles
import json
import re

app = flask.Flask(__name__)
app.debug = True

# db = shelve.open("shorten.db")

# db = {}


db.create_all()




###
# Home Resource:
# Only supports the GET method, returns a homepage represented as HTML
###
@app.route('/', methods=['GET'])
def root():
    """Redirectos to homepage"""
    destination = '/home'
    app.logger.debug("Redirecting to " + destination)
    return flask.redirect(destination)



@app.route('/home', methods=['GET'])
def home():
    """Render the hompepage"""
    # index_title = request.args.get("title", "i253")
    # hello_name = request.args.get("name", "Jim")
    bund = Bundles.query.all()
    links = Links.query.all()
    app.logger.debug("Bundles =>" + str(bund))
    app.logger.debug("Links =>" + str(links))


    return flask.render_template('index.html',responselinks=links, responsebundles=bund)



###
# Wiki Resource:
# GET method will redirect to the resource stored by PUT, by default: Wikipedia.org
# POST/PUT method will update the redirect destination
###
# @app.route('/shorts', methods=['GET'])
# def short():
#     """
#     Show the form page
#     """
#     return flask.render_template('shorten.html')



@app.route('/shorts/<surl>', methods=['GET'])
def short_get(surl):
    """
    Redirect to the shortened url
    """
    surl = str(surl)

    record = Links.query.filter_by(shorturl=surl).first_or_404()

    app.logger.debug("Request : " + str(record.shorturl) + " => " + str(record.longurl))

    return flask.redirect("http://" + record.longurl)




@app.route("/shorts", methods=['PUT', 'POST'])
def short_put():
    """
    create a shortened url for the link
    """
    surl = str(request.form['s'])
    lurl = str(request.form['l'])
    bundle = str(request.form['b'])

    surlrecord = Links.query.filter_by(shorturl=surl).first()

    msg = {}

    responsepage = ''
    if surlrecord is None:
        msg['type'] = 'ERROR'
        msg['txt'] = 'Short URL already exists'

        responsepage = 'response.html'

    else:

        # regex courtesy: http://stackoverflow.com/questions/11242258/strip-url-python
        lurl = re.match(r'(?:\w*://)?(?:.*\.)?([a-zA-Z-1-9]*\.[a-zA-Z]{1,}).*', lurl).groups()[0]

        bund = Bundles(bundle)
        slink = Links(lurl, surl, bund)

        try:
            db.session.add(bund)
            db.session.add(slink)
            db.session.commit()

            msg['type'] = 'Success'
            msg['txt'] = record.longurl + " => " + record.shorturl

            responsepage = 'response.html'

        except:
            db.session.rollback()
            # raise()

            msg['type'] = 'ERROR'
            msg['txt'] = 'Short URL already exists'

            responsepage = 'response.html'



    return flask.render_template(responsepage, msgtype=msg['type'], msgtxt=msg['txt'] )






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

