# -*- coding: utf-8 -*-

"""
    settings
    ~~~~~~~~

    Global settings for project.
"""
import os
from local_settings import LocalConfig
import json

class BaseConfig(LocalConfig):
    _SYSTEM_MESSAGE_CATEGORIES = [
            'success'           # 0 - GREEN
            'info',             # 1 - BLUE
            'warning',          # 2 - YELLOW
            'danger',           # 3 - RED
    ]
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False   
    FILEVIEWER_READONLY = True

    ADMIN_PER_PAGE = 5
    mixedmode = {"name":"htmlmixed"}
    CODEMIRROR_ADDONS = (
      ('display','fullscreen'),
      ('display','placeholder'),            
      ('edit','matchbrackets'),
      ('edit','matchtags'),
      ('edit','closetag'),
      ('comment','comment'),
      ('comment','continuecomment'),
      ('fold','xml-fold'),
    )
      
      
    CODEMIRROR_LANGUAGES = ['css','python','php','javascript','xml','jinja2','htmlmixed','clike','django']
    CODEMIRROR_THEME = 'vibrant-ink'#'blackboard'#'3024-night''vivid-chalk'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    CSRF_ENABLED = True
    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

    URL_MODULES = [
            'core.urls.routes',
            #'admin.urls.routes',
            'flask.ext.xxl.apps.auth.urls.routes',
            'fileviewer.urls.routes',
    ]

    BLUEPRINTS = [
            'core.core',       
            #'admin.admin',
            'flask.ext.xxl.apps.auth.auth',
            #'auth.auth',
            'fileviewer.fileviewer',

    ]

    EXTENSIONS = [
            #'ext.db',
            'ext.admin',
            'ext.toolbar',
            'ext.pagedown',
            'ext.codemirror',
            'ext.alembic',
            #'ext.macro',
    ]

    CONTEXT_PROCESSORS = [
            #'core.context_processors.common_context',
            #'core.context_processors.common_forms',
            'core.context_processors.common_context',
            'auth.context_processors.user_context',
            'core.context_processors.add_is_page',
            'core.context_processors.add_is_list',
            'core.context_processors.add_get_button',
            'core.context_processors.add_get_navbar',
            'core.context_processors.add_get_icon',
            'core.context_processors.add_urlfor',
            'make_base.base',
            'auth.context_processors.auth_context',
            'core.context_processors.add_size_converters',

    ]

    TEMPLATE_FILTERS = [
            'flask.ext.xxl.filters.date',
            'flask.ext.xxl.filters.date_pretty',
            'flask.ext.xxl.filters.datetime',
            'flask.ext.xxl.filters.pluralize',
            'flask.ext.xxl.filters.month_name',
            'flask.ext.xxl.filters.markdown',
            'core.context_processors.fix_body',
            'core.filters.split',
            'core.filters.size',
            'core.filters._sorted',
	    'core.filters.page',
    ]

    CONTACT_FORM_SETTINGS = {
    'HEADING':'Send Us a message',
    'SUBHEADING':'Or a Comment',
    'OPTIONS':(
        ('test','opt1'),
        ('test2','opt2'),
        ('test3','opt3'),
        ('test4','opt4'),
        ('test5','opt5'),
        ('test6','opt6'),
    ),
    'SUBMIT_TEXT':'Send to Us',
    'COMPANY_TITLE':'Level2designs',
    'COMPANY_ADDRESS':{
        'NAME':'level2designs',
        'STREET':'1045 w katella',
        'CITY':'Orange',
        'STATE':'CA',
        'ZIP':'92804',
    },
    'COMPANY_PHONE':'714-783-6369',
    'CONTACT_NAME':'Kyle Roux',
    'CONTACT_EMAIL':'kyle@level2designs.com',
    }


    # populates header option in creating a cms page
    # should be tuples of (name,file)
    NAVBAR_TEMPLATE_FILES = (
            ('bootstrap-std','navbars/bs_std.html'),
            ('bootstrap-inverse','navbars/bs_inverse.html'),
            ('blog','navbars/blog.html'),
            ('clean','navbars/clean.html')
    )


    DEFAULT_NAVBAR = 'clean'

    LAYOUT_FILES = {
            'blog':'layouts/1col_leftsidebar.html',
            'post_form':'layouts/1col_rightsidebar.html',
            'one_col_left':'layouts/1col_leftsidebar.html',
            'one_col_right':'layouts/1col_rightsidebar.html',
            'two_col_left':'layouts/2col_leftsidebar.html',
            'two_col_right':'layouts/2col_rightsidebar.html',
            'three_col_left':'layouts/3col_leftsidebar.html',
    }

    BASE_TEMPLATE_FILES = [
            ('one_col_left','1_col_left.html'),
            ('one_col_right','1_col_right.html'),
            ('two_col_left','2_col_left.html'), 
            ('two_col_right','2_col_right.html'),
            ('three_col','3_col.html'),
    ]

    #BLOG_SIDEBAR_LEFT = False
    #BLOG_SIDEBAR_RIGHT = True
    BLOG_SIDEBAR_LEFT = True
    #BLOG_SIDEBAR_RIGHT = False
    BLOG_TITLE = 'Dynamic'
    BLOG_CONTENT = 'some text to put into my<br />Blog'

    DEFAULT_ICON_LIBRARY = 'octicon'

    SQLALCHEMY_NATIVE_UNICODE = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

def get_choices():
    return BaseConfig.CONTACT_FORM_SETTINGS['OPTIONS']


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing2.db' # 'mysql://test:test@174.140.227.137:3306/test_test5'
