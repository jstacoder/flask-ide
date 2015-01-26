from flask import Blueprint

fileviewer = Blueprint('fileviewer',__name__,
                        template_folder='templates',
                        url_prefix='/view_files')

from flask_ide.fileviewer.views import *


@fileviewer.before_request
def check_dir():
    import os
    import os.path as op
    from settings import BaseConfig
    
    if not op.abspath(os.curdir) == op.abspath(BaseConfig.ROOT_PATH):
        os.chdir(BaseConfig.ROOT_PATH)
