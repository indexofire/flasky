# -*- coding: utf-8 -*-
from google.appengine.ext import db
from blog.utils.taggable import Taggable


class Entry(Taggable, db.Model):
    """
    The entries db table of blog
    """
    title   = db.StringProperty(required=True)
    slug    = db.StringProperty(required=True)
    content = db.TextProperty()
    date    = db.DateTimeProperty(auto_now_add=True)
    #update  = db.DateTimeProperty(auto_now=True)
    #status  = db.StringProperty(required=True, choices=set(["published", "draft"]))

    def __init__(self, parent=None, key_name=None, app=None, **entity_values):
         db.Model.__init__(self, parent, key_name, app, **entity_values)
         Taggable.__init__(self)
