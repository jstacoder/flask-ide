# -*- coding: utf-8 -*-

"""
    app.py
    ~~~~~~

    app initalization
"""
from flask_xxl.main import AppFactory
from flask_macros import FlaskMacro
from settings import DevelopmentConfig
from auth.context_processors import get_navbar

app = AppFactory(DevelopmentConfig).get_app(__name__)
macro = FlaskMacro(app)
#from admin import admin
app.jinja_env.globals['_get_navbar'] = get_navbar
