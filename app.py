#!/usr/bin/env python

# import shelve
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

    # alllinks = {}
    bund = Bundles.query.all()
    links = Links.query.all()

    # app.logger.debug("Bundles =>" + str(bund))
    # for b in bund:

    #     blinks = db.session.query(Links).join(Bundles).filter(Bundles.bundlename==b).all()
    #     alllinks[b] = {
    #         'shorturl' : blinks.shorturl,
    #         'longurl' : blinks.longurl,
    #         'hitcount' : blinks.hitcount
    #     }



    # app.logger.debug("Links =>" + str(links))


    return flask.render_template('index.html',responselinks=links,  responsebundles=bund)



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

    if record is not None:
        dbupdate = Links(record.longurl, record.shorturl, (record.hitcount + 1))

        try:
            db.session.add(dbupdate)
            db.session.commit()
        except:
            db.session.rollback()


        app.logger.debug("Request : " + str(record.shorturl) + " => " + str(record.longurl))

    return flask.redirect("http://" + record.longurl)




@app.route("/shorts", methods=['PUT', 'POST'])
def short_put():
    """
    create a shortened url for the link
    """
    surl = str(request.form['s'])
    lurl = str(request.form['l'])
    # regex courtesy: http://stackoverflow.com/questions/11242258/strip-url-python
    lurl = re.match(r'(?:\w*://)?(?:.*\.)?([a-zA-Z-1-9]*\.[a-zA-Z]{1,}).*', lurl).groups()[0]

    bundle = str(request.form['b'])

    surlrecord = Links.query.filter_by(shorturl=surl).first()

    app.logger.debug("Request : " + " surlrecord: " + str(surlrecord) + " surl :" + str(surl) + " lurl :" + str(lurl))

    msg = {}

    responsepage = 'response.html'

    if surlrecord is not None and surlrecord.shorturl is not None :
        msg['type'] = 'ERROR'
        msg['txt'] = 'Short URL already exists'

    elif surlrecord is not None and surlrecord.longurl is not None:
        msg['type'] = 'ERROR'
        msg['txt'] = 'Long URL already exists'

    else:


        bund = Bundles(bundle)
        slink = Links(lurl, surl, bund)
        app.logger.debug("Creating : " + str(surl) + str(lurl))

        try:

            db.session.add(bund)
            db.session.add(slink)
            db.session.commit()

            msg['type'] = 'Success'
            msg['txt'] = lurl + " => " + surl

        except:
            db.session.rollback()
            # raise()

            msg['type'] = 'ERROR'
            msg['txt'] = 'Database Exception'


    return json.dumps(msg)



@app.route('/bundles', methods=['GET'])
def get_bundles():
    """
    return all the bundles of a user
    """
    allbund = Bundles.query.all()
    bundnames = []
    for b in allbund:
        bundnames.append(str(b).strip())
    bundnames = list(set(bundnames))

    app.logger.debug("bundles: ", bundnames)


    return flask.Response(json.dumps(bundnames), mimetype="application/json")




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

