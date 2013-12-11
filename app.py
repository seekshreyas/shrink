#!/usr/bin/env python

# import shelve
from subprocess import check_output
import flask
from flask import request
# from os import environ

import re

app = flask.Flask(__name__)
app.debug = True

db = shelve.open("shorten.db")

# db = {}


###
# Home Resource:
# Only supports the GET method, returns a homepage represented as HTML
###
@app.route('/', methods=['GET'])
def home():
    """Builds a template based on a GET request, with some default
    arguements"""
    index_title = request.args.get("title", "i253")
    hello_name = request.args.get("name", "Jim")
    return flask.render_template(
            'index.html',
            title=index_title,
            name=hello_name)


###
# Wiki Resource:
# GET method will redirect to the resource stored by PUT, by default: Wikipedia.org
# POST/PUT method will update the redirect destination
###
@app.route('/wiki', methods=['GET'])
def wiki_get():
    """Redirects to wikipedia."""
    destination = db.get('wiki', 'http://en.wikipedia.org')
    # destination = http://en.wikipedia.org'
    app.logger.debug("Redirecting to " + destination)
    return flask.redirect(destination)

@app.route("/wiki", methods=['PUT', 'POST'])
def wiki_put():
    """Set or update the URL to which this resource redirects to. Uses the
    `url` key to set the redirect destination."""
    wikipedia = request.form.get('url', 'http://en.wikipedia.org')
    db['wiki'] = wikipedia
    return "Stored wiki => " + wikipedia



###
# Wiki Resource:
# GET method will redirect to the resource stored by PUT, by default: Wikipedia.org
# POST/PUT method will update the redirect destination
###
@app.route('/shorts', methods=['GET'])
def short():
    """
    Show the form page
    """
    return flask.render_template('shorten.html')



@app.route('/shorts/<surl>', methods=['GET'])
def short_get(surl):
    """
    Redirect to the shortened url
    """
    shorturl = str(surl)

    msg = {}
    if db.has_key(shorturl):
        app.logger.debug("Redirect to =>" + db[shorturl])

        return flask.redirect("http://" + db[shorturl])
    else:
        msg['type'] = 'ERROR'
        msg['txt'] = 'Short url doesnt exist'

        return flask.render_template('response.html',
                                    msgtype=msg['type'],
                                    msgtxt=msg['txt'] )



@app.route("/shorts", methods=['PUT', 'POST'])
def short_put():
    """
    create a shortened url for the link
    """
    shorturl = str(request.form['s'])
    longurl = str(request.form['l'])




    msg = {}
    if db.has_key(shorturl):
        msg['type'] = 'ERROR'
        msg['txt'] = 'Short URL already exists'


    else:

        # regex courtesy: http://stackoverflow.com/questions/11242258/strip-url-python
        longurl = re.match(r'(?:\w*://)?(?:.*\.)?([a-zA-Z-1-9]*\.[a-zA-Z]{1,}).*', longurl).groups()[0]

        db[shorturl] = longurl

        msg['type'] = 'Success'
        msg['txt'] = db[shorturl] + " => " + shorturl

    return flask.render_template('response.html',
                                    msgtype=msg['type'],
                                    msgtxt=msg['txt'] )

###
# i253 Resource:
# Information on the i253 class. Can be parameterized with `relationship`,
# `name`, and `adjective` information
#
# TODO: The representation for this resource is broken. Fix it!
# Set the correct MIME type to be able to view the image in your browser
##/
@app.route('/i253')
def i253():
    """Returns a PNG image of madlibs text"""
    relationship = request.args.get("relationship", "friend")
    name = request.args.get("name", "Jim")
    adjective = request.args.get("adjective", "fun")

    resp = flask.make_response(
            check_output(['convert', '-size', '600x400', 'xc:transparent',
                '-frame', '10x30',
                '-font', '/usr/share/fonts/liberation/LiberationSerif-BoldItalic.ttf',
                '-fill', 'black',
                '-pointsize', '32',
                '-draw',
                  "text 30,60 'My %s %s said i253 was %s'" % (relationship, name, adjective),
                '-raise', '30',
                'png:-']), 200);
    # Comment in to set header below
    resp.headers['Content-Type'] = 'image/png'

    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
