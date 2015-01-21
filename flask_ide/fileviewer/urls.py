from . import fileviewer
from .views import FileView,MsgView,TestView
from ._json import JsonCodeView,JsonFileView,LoginView

routes = [
        ((fileviewer),
            ('',FileView.as_view('view_files')),
            ('/<item_name>',FileView.as_view('files')),
            ('/json',JsonCodeView.as_view('json')),
            ('/file/<path:file_name>',JsonFileView.as_view('file')),
            ('/msgs',MsgView.as_view('msgs')),
            ('/login',LoginView.as_view('login')),
            ('/test',TestView.as_view('test')),
            ('/account/<int:id_num>',TestView.as_view('view_account')),

)]
