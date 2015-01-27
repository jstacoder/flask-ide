# -*- coding: utf-8 -*-

"""
    ext.py
    ~~~
    :license: BSD, see LICENSE for more details
"""

from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.wtf import Form
from flask.ext.codemirror import CodeMirror
from flask.ext.pagedown import PageDown
#from flask.ext.script import Manager
from flask.ext.alembic import Alembic
from flask_admin import Admin


#manager = Manager()
pagedown = PageDown()
#db.engine.connection
codemirror = CodeMirror()
alembic = Alembic()
admin = Admin(template_mode='bootstrap3')
# Almost any modern Flask extension has special init_app()
# method for deferred app binding. But there are a couple of
# popular extensions that no nothing about such use case.

toolbar = lambda app: DebugToolbarExtension(app)  # has no init_app()
