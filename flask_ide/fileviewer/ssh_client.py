# coding: utf-8
import paramiko
import sys
import json
from time import sleep


class SFTPConnection(object):

    _user = None
    _password = None
    _host = '127.0.0.1'

    _c = None

    def __init__(self,**kwargs):
        if 'username' in kwargs:
            self._user = kwargs.pop('username')
        if 'password' in kwargs:
            self._password = kwargs.pop('password')
        if 'host' in kwargs:
            self._host = kwargs.pop('host')
        self.kwargs = kwargs
        self._c = self.sftp

    @property
    def conn(self):
        rtn = login(self._user,self._password,self._host)
        return rtn

    @property
    def sftp(self):
        self._conn = self.conn
        self._sftp = self._conn.open_sftp()
        return self._sftp

    def __getattr__(self,name):
        if name in globals():
            return globals()[name]
        if name in dir(self._sftp):
            return getattr(self._sftp,name)
        if name in locals():
            return locals()[name]
        return None

    def is_file(self,f,search_files=True,hidden=False):
        rtn = True
        if f is None:
            return False
        if not hidden:
            if f.startswith('.'):
                rtn = False
        if rtn:
            f = '"{}"'.format(f)
            cmd = "python -c " + '"import os; os.path.isfile(' +"'"+ f +"'"+ ')"'
            si,so,se = self._conn.exec_command(cmd)
            error = se.read().strip()
            if error == '':
                res = so.read()
                if 'True' in res:
                    if search_files:
                        rtn = True
                    else:
                        rtn = False
                else:
                    if search_files:
                        rtn = False
                    else:
                        rtn = True
            else:
                raise Exception(error)            
        return res

    def isfile(self,f,*args,**kwargs):
        return self.is_file(f,*args,**kwargs)
        
    def is_dir(self,f):
        return self.is_file(f,False)

    def isdir(self,f,*args,**kwargs):
        return self.is_dir(f,*args,**kwargs)


    def listdir(self,name='.'):
        def add_(itm):
            a,b = itm[0],itm[1]
            rtn = a + b if a.endswith('/') else a + '/' + b
            return rtn
        
        if self.is_dir(name):
            res = self._sftp.listdir(name)
            if name != '.':
                rtn = filter(add_,zip([name]*len(res),res))
            else:
                rtn = res
        else:
            rtn = name
        return rtn


class SSHFileBrowser(object):

    def __init__(self,user,password,host,base_dir):
        self.username = user
        self.password = password
        self.host = host
        self.base_dir = base_dir
        self.ssh = SFTPConnection(
                        username=self.username,
                        password=self.password,
                        host=self.host,
        )

    def split_files_and_dirs(self,dirname):
        data = self.list_dir(dirname)
        files,dirs = [],[]
        for itm in data:
            tmp = dirname+'/'+itm
            if self.is_dir(tmp):
                dirs.append(itm)
            else:
                files.append((itm,tmp))
        return files,dirs

        

    
    def filter_files(files):
        rtn = []
        for f in files:
            end = f.split('.')[-1]
            if end in IGNORE_EXTENSIONS:
                pass
            else:            
                rtn.append((op.basename(f),op.relpath(f)))
        return rtn
    

    def list_dir(self,d):
        try:
            rtn = self.ssh.listdir( #map(
                # lambda x: x[1] if len(x) >= 2 else x,
                    self.base_dir + (
                        '/' if not self.base_dir.endswith('/'
                        ) else ''
                    ) + d
                )
            return rtn
        except:
            pass
        

    def is_dir(self,d):
        return self.ssh.isdir(self.base_dir + ('/' if not self.base_dir.endswith('/') else '') + d)

    def is_file(self,f):
        return self.ssh.isfile(self.base_dir + ('/' if not self.base_dir.endswith('/') else '') + f)

    def cur_dir(self):
        return self.ssh.getcwd() or self.base_dir

    def dir_name(self,item):
        cmd = 'python -c "import os; print os.path.dirname(os.path.abspath('+item+'))"'
        i,o,e = self.ssh._conn.exec_command(cmd)
        return o.read().strip()

    def load_file(self,name):
        return self.ssh.sftp.open(name,'read').read()

    def save_file(self,name,data,append=False):
        mode = 'w'
        if append:
            mode = 'a'
            old_data = self.load_file(name)
        with self.ssh.open(name,mode) as f:
            f.write(data)
        return self.load_file(name) == data if not append else self.load_file(name) == old_data + data

    def exists(self,name):
        result = False
        try:
            self.ssh.open(name,'r')
            result = True
        except IOError:
            pass
        return result


class _SSH(object):
    _conn = None

    @classmethod
    def split_files_and_dirs(cls,name):
        return cls._conn.split_files_and_dirs(name)
        
    @classmethod
    def is_dir(cls,name):
        return cls._conn.is_dir(name)

    @classmethod
    def is_file(cls,name):
        return cls._conn.is_dir(name)

    @classmethod
    def cur_dir(cls):
        return cls._conn.cur_dir()

    @classmethod
    def list_dir(cls,name):
        return cls._conn.list_dir(name)

    @classmethod
    def dir_name(cls,name):
        return cls._conn.dir_name(name)

    @classmethod
    def load_file(cls,name):
        return cls._conn.ssh.sftp.open(name,'r').read()

    @classmethod
    def save_file(cls,name):
        return cls._conn.save_file(name)

    @classmethod
    def exists(cls,name):
        return cls._conn.exists(name)

def get_ssh_class(*args,**kwargs):
    conn = SSHFileBrowser(*args,**kwargs)
    return type('sshclass',(_SSH,),dict(_conn=conn))

def get_connection(host,username,password,**kwargs):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,username=username,password=password,**kwargs)
    return ssh

def get_sftp(conn):
    sftp = conn.open_sftp()
    return sftp


def process_dir(dirname):
    return dirname

def process_dirs(dirs):
    return '\n'.join(map(process_dir,dirs))


def login(user,password,host,**kwargs):
    if 'base_dir' in kwargs:
        kwargs.pop('base_dir')
    conn = get_connection(host,user,password,**kwargs)
    return conn

def _sftp():
    rtn = login()
    sleep(5)
    sftp = get_sftp(rtn)
    return sftp
   

def main():
    if len(sys.argv) > 1:
        dirname = sys.argv[1]
    else:
        dirname = None

    conn = login()
    sftp = get_sftp(conn)
    rtn = sftp.listdir() if dirname is None else sftp.listdir(dirname)
    return process_dirs(rtn)


if __name__ == "__main__":
    main()
