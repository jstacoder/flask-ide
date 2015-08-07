from ext import admin
from flask_admin import AdminIndexView,BaseView
from flask_admin.contrib.sqla.view import ModelView
from flask_ide.core.models import Account,Server,ConnectionType,UserProfile
from flask_xxl.apps.auth.models import User,Role
from app import app

class AccountAdmin(ModelView):
    def __init__(self,*args,**kwargs):
        super(AccountAdmin,self).__init__(Account,*args,**kwargs)
    
    def is_accessible(self):
        return False

class ServerAdmin(ModelView):
    inline_models = (Account,)

    def __init__(self,*args,**kwargs):
        super(ServerAdmin,self).__init__(Server,*args,**kwargs)
    
    def is_accessible(self):
        return False

class ConnectionTypeAdmin(ModelView):
    def __init__(self,*args,**kwargs):
        super(ConnectionTypeAdmin,self).__init__(ConnectionType,*args,**kwargs)
    
    def is_accessible(self):
        return False

class UserProfileView(ModelView):
    def __init__(self,*args,**kwargs):
        super(UserProfileView,self).__init__(UserProfile,UserProfile.session,category='Users',*args,**kwargs)
    
    def is_accessible(self):
        return False

class UserView(ModelView):
    inline_models = (UserProfile,)
    def __init__(self,*args,**kwargs):
        super(UserView,self).__init__(User,User.session,category='Users',*args,**kwargs)
    
    def is_accessible(self):
        return False

class RoleAdmin(ModelView):
    def __init__(self,*args,**kwargs):
        super(RoleAdmin,self).__init__(Role,Role.session,category='Users',*args,**kwargs)
    
    def is_accessible(self):
        return False

    

with app.test_request_context():
    admin.add_view(AccountAdmin(Account.session,category='Connections'))
    admin.add_view(ServerAdmin(Server.session,category='Connections'))
    admin.add_view(ConnectionTypeAdmin(ConnectionType.session,category='Connections'))
    admin.add_view(UserProfileView())
    admin.add_view(UserView())
