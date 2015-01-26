from flask_xxl.baseviews import BaseView
from flask import request,jsonify,session
from flask_ide.fileviewer.forms import CodeForm
from flask_ide.settings import DevelopmentConfig
from flask_ide.fileviewer.handlers import handlers
from flask_ide.core.models import Account

root = DevelopmentConfig.ROOT_PATH

IGNORE_EXTENSIONS = ['pyc','swp','db','pid','zip']
ACCEPT_EXTENSIONS = ['.py','.html','.css','.js','.sh']

def get_editor_mode(name):
    modes = {
        'py':'python',
        'html':'django',
        'php':'php',
        'js':'javascript',
        'txt':'text',
    }
    return modes.get(name.split('.')[-1],None) or 'python'

class MsgView(BaseView):
        _template = 'messages.html'

        def get(self):
            self.flash('just a test flash','success')
            result = self.render()
            return jsonify(result=result)

class TestView(BaseView):
    def post(self,id_num=None):
        session.pop('ssh_auth',None) #= dict(user='root',pw='1414Wp8888!',host='174.140.227.137',base_dir='/')
        session.pop('handler',None) 
        return self.redirect('fileviewer.view_files')
        if id_num is not None:
            account = Account().query.get(id_num)
            if account is not None:
                session['ssh_auth'] = dict(user=account.username,pw=account.password,host=account.server.ip_address,base_dir=account.base_dir)
                session['handler'] = 'ssh'

class FileView(BaseView):
    _file_handler = None
    _template = 'view_files.html'
    _context = {'files':[],'dirs':[],'file_content':'','body_style':'margin-top:100px;'}

    def _split_files_and_dirs(self,dirname):
        return self._file_handler.split_files_and_dirs(dirname)

    def _is_dir(self,item):
        return self._file_handler.is_dir(item)
    
    def _cur_dir(self):
        return self._file_handler.cur_dir()

    def _list_dir(self,item):
        return self._file_handler.list_dir(item)

    def _dir_name(self,item):
        return self._file_handler.dir_name(item)

    def _load_file(self,item):
        return self._file_handler.load_file(item)

    def _exists(self,item):
        return self._file_handler.exists(item)

    def _save_file(self,name,content):
        return self._file_handler.save_file(name,content)

    def get(self,item_name=None):
        if item_name is not None:
            item_name = item_name
        if 'var' in session:
            return 'ok'
        handler = 'local'
        if 'handler' in session:
                handler = session['handler']
        self._file_handler = handlers[handler]
        if 'ssh_auth' in session:
            self._file_handler = self._file_handler(**session['ssh_auth'])
        item_name = request.args.get('item_name',None)
        if item_name is None:
            # get inital dir and file list to display
            try:
                d = self._file_handler._conn.base_dir 
            except:
                d = root
            self._context['files'],self._context['dirs'] = self._split_files_and_dirs(d)
            self._context['root'] = d
        else:
            # find out if its a dir or a file
            is_file = False
            if not self._is_dir(item_name):
                is_file = True
            if not is_file:
                # is dir, list files
                self._context['files'],self._context['dirs'] = self._split_files_and_dirs(item_name)            
                self._context['current_dir'] = item_name or '/'
            else:
                # is file, edit
                self._template = 'file_editor.html'
                # get all files in current directory, with filters 
                if item_name is None or item_name == '':
                    item_name = self._cur_dir()
                self._context['other_files'] = [str(x) for x in self._list_dir(
                    		                    self._dir_name(item_name) or root
                                                    ) if '.' + x.split(
                                                         '.'
                                                    )[-1] in ACCEPT_EXTENSIONS\
                                                    or x.startswith(
                                                         '.'
                                                    ) and self._is_file(x)
                                               ]
                if len(item_name.split('/')) == 2 and not all(item_name.split('/')):
                    if item_name.startswith('/'):
                        item_name = item_name[1:]
                self._context['file_content'] = self._load_file(item_name)
                self._context['file_name'] = item_name
                self._form_args = {'file_name':item_name}
                self._context['editor_mode'] = get_editor_mode(item_name)
                self._form = CodeForm
        return self.render()


    def post(self):
        handler = 'local'
        if 'handler' in session:
                handler = session['handler']
        self._file_handler = handlers[handler]
        content = request.form.get('content')
        name = request.form.get('file_name')
        self._context['file_name'] = name
        self._template = 'save_file.html'
        self._context['content'] = content
        self._context['exists'] = self._exists(name) and self._is_file(name)
        if self._save_file(name,content):
            self.flash('successfully saved {}'.format(name))
        else:
            self.flash('Error saving {}'.format(name),'danger')
        return self.redirect('fileviewer.view_files')
