#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Manage
=========

Manage and run the flask environment


author = "Shreyas"
email = "shreyas@ischool.berkeley.edu"
python_version = "Python 2.7.5 :: Anaconda 1.6.1 (x86_64)"
"""

from flask.ext.script import Manager
import shrinkdb

manager = Manager(shrinkdb)



if __name__ == '__main__':
    manager.run()
