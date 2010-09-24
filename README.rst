A Flask_ diary app built on GAE_ as a Flask Learning Homework
===============================================================

.. _Flask: http://flask.pocoo.org/
.. _GAE: http://code.google.com/appengine/

1. install:
--------------

* get the source code:

$ git clone git://github.com/indexofire/flasky.git

* change the code fitting for you

2. usage:
--------------

* change your admin username and password

flasky/blog/settings.py:

change the `USERNAME` and `PASSWORD` as what you want.

* upload to google app engine

$ python2.5 /path/to/google_appengine/appcfg.py upload flasky/flasky/

login as: admin/123456 or the setup what you changed before, into dashboard to 
publish article.
