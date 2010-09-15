# -*- coding: utf-8 -*-
from flask import Flask
import settings
app = Flask('blog')
app.config.from_object('blog.settings')

from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import abort
from flask import flash
from flask import session
from flask import get_flashed_messages
from google.appengine.ext import db

import settings

DEBUG             = True
CSRF_ENABLED      = True
SECRET_KEY        = '64Qj&f62Fa(fa&_A98a0-1ZlkfFaGz9A$69'
CSRF_SESSION_LKEY = '69JFJ^$(D#!S;LKdeh8asSNJ283403808=+'
USERNAME          = 'indexofire'
PASSWORD          = '78100188274867'




class Entry(db.Model):
    """
    The entries db table of blog
    """
    title = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)


@app.route('/')
def index():
    entries = db.GqlQuery("SELECT * FROM Entry ORDER BY date DESC LIMIT 10")
    return render_template('index.html', entries=entries)


@app.route('/entry/<int:id>')
def entry():
    entry = Entry.get_by_id(id)
    return render_template('entry.html', entry=entry)


@app.route('/add', methods=['POST'])
def add():
    if not session.get('logged_in'): abort(401)
    entry = Entry()
    entry.title   = request.form['title']
    entry.content = request.form['content']
    if not entry.title:
        flash("You forget to name a blog!")
        return redirect(url_for('index'))
    if not entry.content:
        flash("Bad idea! You leave blank to your blog!")
        return redirect(url_for('index'))
    entry.put()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
