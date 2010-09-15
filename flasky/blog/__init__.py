# -*- coding: utf-8 -*-
from flask import Flask
import settings

app = Flask(__name__)
app.config.from_object('blog.settings')

import application
import api
