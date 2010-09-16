# -*- coding: utf-8 -*-
from google.appengine.ext import db
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import abort
from flask import flash
from flask import session
from flask import get_flashed_messages
from blog import app
app.config.from_object('blog.settings')

class Entry(db.Model):
    """
    The entries db table of blog
    """
    title   = db.StringProperty()
    content = db.TextProperty()
    slug    = db.StringProperty()
    date    = db.DateTimeProperty(auto_now_add=True)
    #status  = db.StringProperty(required=True, choices=set(["published", "draft"]))

class Tag(db.Model):
    """
    The tags model
    """
    pass
    
@app.route('/')
def index():
    entries = db.GqlQuery("SELECT * FROM Entry ORDER BY date DESC LIMIT 10")
    return render_template('index.html', entries=entries)


@app.route('/entry/<int:id>')
def entry(id):
    entry = Entry.get_by_id(id)
    if not entry:
        return redirect(url_for('index'))
    return render_template('entry.html', entry=entry)


@app.route('/dashboard/')
def dashboard():
    pass


@app.route('/add', methods=['POST'])
def add():
    if not session.get('logged_in'): abort(401)
    title   = request.form['title']
    content = request.form['content']
    #slug    = request.form['slug']
    if not title:
        flash("You forget to name a blog!")
        return redirect(url_for('index'))
    if not content:
        flash("Bad idea! You leave blank to your blog!")
        return redirect(url_for('index'))
    entry = Entry(title=title, content=content)
    entry.put()
    return redirect(url_for('index'))


@app.route('/entry/<int:id>/delete')
def delete(id):
    entry = Entry.get_by_id(id)

#@app.route('/entry/<int:id>/edit')
    
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
