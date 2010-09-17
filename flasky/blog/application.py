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
from blog.models import Entry


@app.route('/')
def index():
    entries = db.GqlQuery("SELECT * FROM Entry ORDER BY date DESC LIMIT %s" % app.config['ARTICLE_PERPAGE'])
    return render_template('index.html', entries=entries)


@app.route('/archive')
def archive():
    entries = Entry.all()
    return render_template('archive.html', entries=entries)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not session.get('logged_in'):
        abort(401)
    entry = Entry.get_by_id(id)
    if request.method == 'POST':
        entry.title   = request.form['title']
        entry.content = request.form['content']
        entry.slug    = request.form['slug']
        entry.put()
        return redirect(url_for('index'))
    else:
        return render_template('edit.html', entry=entry)


@app.route('/entry/<int:id>')
def entry(id):
    error = None
    entry = Entry.get_by_id(id)
    if not entry:
        error = "Can't find the blog entry"
        return render_template('error.html', error=error)
    return render_template('entry.html', entry=entry)


@app.route('/add', methods=['POST'])
def add():
    if not session.get('logged_in'):
        abort(401)
    title   = request.form['title']
    content = request.form['content']
    slug    = request.form['slug'].strip().lower()
    tags    = request.form['tags']
    if not title:
        flash("You forget to name a blog!")
        return redirect(url_for('index'))
    if not content:
        flash("Bad idea! You leave blank to your blog!")
        return redirect(url_for('index'))
    if not slug:
        flash(tags)
        return redirect(url_for('index'))
    entry = Entry(title=title, slug=slug, content=content, tags=tags)
    entry.put()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('logged_in'):
        abort(401)
    entry = Entry.get_by_id(id)
    if not entry:
        error = "Can't find the blog entry"
        return render_template('error.html', error=error)
    q = db.GqlQuery("SELECT * FROM Entry WHERE title = '%s' " % entry.title)
    if q:
        e = q.fetch(1)
        db.delete(e)
        flash("You have done deletion!")
        return redirect(url_for('index'))
    else:
        error = "Can't find the blog entry"
        return render_template('error.html', error=error)


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        abort(401)
    return render_template('dashboard.html')

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
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
