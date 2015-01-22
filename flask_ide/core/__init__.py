# -*- coding: utf-8 -*-
from flask import Blueprint

__package__ = 'core'


core = Blueprint('core', __name__,
                 template_folder='templates',
                 url_prefix='/')


from core  import views
from core  import errors


