# -*- coding: utf-8 -*-
from datetime import datetime
from urlparse import urljoin
from google.appengine.ext import db
from flask import render_template, redirect, url_for, request, abort
from flask import flash, session, get_flashed_messages
from werkzeug.contrib.atom import AtomFeed
from blog import app
from blog.models import Entry


def make_external(url):
    return urljoin(request.url_root, url)

@app.route('/recent')
def recent_feed():
    feed = AtomFeed("Mark Renton's Blog", feed_url=request.url, url=request.url_root)
    query = Entry.all().order('-date').fetch(20)
    for q in query:
        feed.add(
            q.title,
            unicode(q.content),
            content_type='html',
            url=make_external(q.slug),
            updated=q.date,
        )
    return feed.get_response()

@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    now = datetime.utcnow()
    diff = now - dt
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )
    for period, singular, plural in periods:
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)
    return default

@app.route('/')
def index():
    entries = db.GqlQuery("SELECT * FROM Entry ORDER BY date DESC LIMIT %s" % app.config['ARTICLE_PERPAGE'])
    return render_template('index.html', entries=entries)


@app.route('/archive')
def archive():
    entries = Entry.all().order('-date')
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

@app.route('/entry/<slug>')
def entry(slug):
    error = None
    entry = Entry.gql("WHERE slug = :1 ", slug)
    if not entry:
        error = "Can't find the blog entry"
        return render_template('error.html', error=error)
    return render_template('entry.html', entry=entry[0])

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
