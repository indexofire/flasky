# -*- coding: utf-8 -*-
from flask import Flask
import settings

DEBUG             = True
CSRF_ENABLED      = True
SECRET_KEY        = '64Qj&f62Fa(fa&_A98a0-1ZlkfFaGz9A$69'
CSRF_SESSION_LKEY = '69JFJ^$(D#!S;LKdeh8asSNJ283403808=+'
USERNAME          = 'indexofire'
PASSWORD          = '78100188274867'

app = Flask('blog')
app.config.from_object('blog')

