# -*- coding: utf-8 -*-
from flask import Flask
app = Flask('blog')
app.config.from_object('blog.settings')
