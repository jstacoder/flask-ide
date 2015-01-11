# -*- coding: utf-8 -*-

"""
    app.py
    ~~~~~~

    app initalization
"""
from main.factory import AppFactory
from settings import DevelopmentConfig
from core.context_processors import get_navbar

app = AppFactory(DevelopmentConfig).get_app(__name__)


app.jinja_env.globals['_get_navbar'] = get_navbar
