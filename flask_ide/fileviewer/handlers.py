from settings import DevelopmentConfig
import os.path as op
import os

root = DevelopmentConfig.ROOT_PATH

IGNORE_EXTENSIONS = ['pyc','swp','db','pid','zip']
ACCEPT_EXTENSIONS = ['.py','.html','.css','.js','.sh']

class BaseFileHandler(object):

    def split_files_and_dirs(self,dirname):
        '''
        files,dirs = '',''
        return tuple(files,dirs)
        '''
        raise NotImplemented

    def is_dir(self,item):
        '''
        return bool
        '''
        raise NotImplemented

    def is_file(self,item):
        '''
        return bool
        '''
        raise NotImplemented

    def cur_dir(self):
        '''
        return str
        '''
        raise NotImplemented

    def list_dir(self,dirname):
        '''
        return list
        '''
        raise NotImplemented

    def dir_name(self,item):
        '''
        return str
        '''
        raise NotImplemented
    
    def load_file(self,name):
        '''
        return str
        '''
        raise NotImplemented

    def save_file(self,name,data):
        '''
        return bool
        '''
        raise NotImplemented

    def exists(name):
        '''
        return bool
        '''
        raise NotImplemented


def save_file(name,content):
    old = open(name,'r').read()
    if old.strip() != content.strip():
        with open(name,'w') as f:
            f.write(content)
        return True
    return False

def get_editor_mode(name):
    modes = {
        'py':'python',
        'html':'django',
        'php':'php',
        'js':'javascript',
        'txt':'text',
    }
    return modes[name.split('.')[-1]] or 'python'

def filter_files(files):
    rtn = []
    for f in files:
        end = f.split('.')[-1]
        if end in IGNORE_EXTENSIONS:
            pass
        else:            
            rtn.append((op.basename(f),op.relpath(f)))
    return rtn

def split_files_and_dirs(dirname):
    contents = os.listdir(dirname)
    files,dirs = [],[]
    for itm in contents:
        tmp = op.join(dirname,itm)
        if op.isdir(tmp):
            dirs.append(itm)
        else:            
            files.append(op.join(dirname,itm))
    return filter_files(files),dirs

class LocalHandler(BaseFileHandler):
    @staticmethod
    def split_files_and_dirs(dirname):
        return split_files_and_dirs(dirname)

    @staticmethod
    def is_dir(item):
        return op.isdir(item)

    @staticmethod
    def is_file(item):
        return op.isfile(item)

    @staticmethod
    def cur_dir():
        return os.getcwd()

    @staticmethod
    def list_dir(dirname):
        return os.listdir(dirname)

    @staticmethod
    def dir_name(item):
        return op.dirname(op.abspath(item))

    @staticmethod
    def load_file(name):
        return open(name,'r').read()

    @staticmethod
    def save_file(name,data,append=False):
        mode = 'w'
        if append:
            mode = 'a'
            old_data = LocalHandler.load_file(name)
        with open(name,mode) as f:
            f.write(data)
        return LocalHandler.load_file(name) == data if not append else LocalHandler.load_file(name) == old_data + data

    @staticmethod
    def exists(name):
        return op.exists(name)

handlers = dict(
    local=LocalHandler,
)
