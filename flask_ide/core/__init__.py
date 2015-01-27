# -*- coding: utf-8 -*-
from flask import Blueprint

#__package__ = 'core'


core = Blueprint('core', __name__,
                 template_folder='templates',
                 url_prefix='/')


from . import views # flask_ide.core import views
from . import errors #flask_ide.core import errors


