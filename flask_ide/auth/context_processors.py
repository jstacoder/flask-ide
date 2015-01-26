from flask import session

def user_context():
    if 'email' in session:
        if 'user_id' in session:
            from auth.models import User
            return {
                'user':User.get_by_id(session.get('user_id',None)),
                'email':session.get('email',None)
            }
    return {'user':None}

def auth_context():
    logged_in = False 
    return {'logged_in':session.get('logged_in',logged_in)}
import os
from markdown import Markdown
from flask_ide.settings import BaseConfig
from flask.helpers import url_for
from flask import session
from flask_ide.fileviewer.handlers import handlers
#from faker.factory import Factor


ROOT_PATH = BaseConfig.ROOT_PATH
root = ROOT_PATH


def get_navbar(name):
    fmt = 'navbars/{}.html'
    navmap = {
        'bs3':'bs3_std',
        'inverse':'bs_inverse',
        'bootstrap-inverse':'bs_inverse',
        'blog':'blog',
        'clean':'clean',
        
    }
    return fmt.format(navmap[name])

def add_get_navbar():
    return {'_gat_navbar':get_navbar}


def get_button(*args,**kwargs):
    return Markdown('<a class="btn btn-default">a</a>')

def add_get_button():
    return {'get_button':get_button}

def add_get_icon():
    return {'get_icon':lambda name,lib='glyphicon':'<span class="{0} {0}-{1}></span>'.format(lib,name)}

def add_urlfor():
    return {'url_for':url_for}

def get_dir_files(dirname):
    if not dirname:
        return []
    if 'ssh_auth' in session:
        file_handler = handlers['ssh'](**session['ssh_auth'])
    else: 
        file_handler = handlers['local']
    if file_handler.is_dir(dirname):
        return file_handler.list_dir(dirname)
    raise IOError

def is_list(lst):
    return type(lst) == list


def add_is_list():
    return {'is_list': is_list}

def _get_name():
    #factory = Factory()
    #faker = factory.create()
    return ''#faker.name()
    
#return 'kyle'

get_parent_path = lambda: os.path.relpath(os.curdir,start=root)


def is_dir(name):
    if 'ssh_auth' in session:
        file_handler = handlers['ssh'](**session['ssh_auth'])
        return file_handler.is_dir(name)
    else: 
        file_handler = handlers['local']
        return file_handler.is_dir(os.path.join(ROOT_PATH,name))

def extract_settings(config):
    rtn = []
    for itm in sorted(config.__dict__.keys()):
        if not itm.startswith('_') and itm == itm.upper():
            pass
            #rtn.append((itm,config.get(itm,'x')),)
        else:
            if not itm.startswith('__') and not len(itm.split('_'))<3:
                group,setting = itm.split('_')[1],'_'.join(itm.split('_')[2:])
                rtn.append((setting,itm))
    return tuple(rtn)

def get_pages(lst,per_page=10):
    rtn = []
    new_lst = list(reversed(lst))
    page_total = len(lst) / per_page
    if len(lst) % per_page != 0:
        page_total += 1
    pages = [list() for x in range(page_total)]
    count = 0
    for new_page in pages:
        while count != per_page:
            if new_lst:
                count += 1
                new_page.append(new_lst.pop())
            else:
                break
        count = 0                    
    return pages
            
def common_context():
    return {
        'parent_path':get_parent_path,
        'list_dir':get_dir_files,
        'get_pages':get_pages,
        'unicode':unicode,
        'getattr':getattr,
        'extract_settings':extract_settings,
        'str':str,
        'zip':zip,
        'is_dir':is_dir,
        'my_email': 'kyle@level2designs.com',
        'type': type,
        'dir': dir,
        'get_name': _get_name,
        'use_editor': False,
        'config':BaseConfig,
        'map':map,
    }


def common_forms():
    return {}   


def is_page(obj):
    return obj.__class__.__name__ == 'Page'


def add_is_page():
    return {'is_page': is_page}


#ef add_get_button():
#   return {'get_button': get_button}


def get_model(model, blueprint=None):
    if '_' in model:
        start, end = model.split('_')
        cls = start.title() + end.title()
    else:
        cls = model.title()
    return __import__(blueprint or model.lower() +
                      '.models', globals(), locals(),
                      fromlist=[]).models.__dict__[cls]


def add_get_model():
    return {'get_model': get_model}


def fix_body(txt):
    return txt.replace('.','_')


def add_layouts():
    layouts = BaseConfig.LAYOUT_FILES.copy()
    return dict(layouts=layouts)
            

def layout_menu():
    return '''
    <div class=layout-menu>
        <div class=row>
            <div class=col-md-4>
                <div class=list-group>
                    <a class="list-group-item" href="{{url_for('.blockview',alt_layout=3)}}">3 columns</a>
                </div>
            </div>
            <div class=col-md-4>
                <div class=list-group>
                    <a class="list-group-item" href="{{url_for('.blockview',alt_layout=4)}}">4 columns</a>
                </div>
            </div>
            <div class=col-md-4>
                <div class=list-group>
                    <a class="list-group-item" href="{{url_for('.blockview',alt_layout=5)}}">5 columns</a>
                </div>
            </div>
        </div>
    </div>
    '''

def add_layout_mode():
    return dict(layout_menu=layout_menu)


def convert_size(base,size):
    size_map = {
        'md': {
            '12':'14',
            '10':'10',
            '9':'9',
            '8':'8',
            '6':'6',
            '5':'5',
            '4':'4',
            '3':'3',
            '2':'2',
            '1':'2',
        },
        'xs': {
            '16':'12',
            '14':'9',
            '12':'8',
            '10':'7',
            '8':'6',
            '6':'4',
            '3':'2',
            '2':'1',
        }
    }
    return size_map[base][str(size)]
        

def get_alt_base(base):
    return 'md' if base == 'xs' else 'xs'

def add_size_converters():
    return dict(convert_size=convert_size,get_alt_base=get_alt_base)

