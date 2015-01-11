from . import fileviewer
from .views import FileView,MsgView
from .json import JsonCodeView,JsonFileView

routes = [
        ((fileviewer),
            ('',FileView.as_view('view_files')),
            ('/<item_name>',FileView.as_view('files')),
            ('/json',JsonCodeView.as_view('json')),
            ('/file/<path:file_name>',JsonFileView.as_view('file')),
            ('/msgs',MsgView.as_view('msgs')),
)]
