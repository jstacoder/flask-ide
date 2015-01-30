from ext import admin
from flask_admin import AdminIndexView,BaseView
from flask_admin.contrib.sqla.view import ModelView
from flask_ide.core.models import Account,Server,ConnectionType
from app import app

class AccountAdmin(ModelView):
    def __init__(self,*args,**kwargs):
        super(AccountAdmin,self).__init__(Account,*args,**kwargs)

class ServerAdmin(ModelView):
    

    def __init__(self,*args,**kwargs):
        super(ServerAdmin,self).__init__(Server,*args,**kwargs)


    
class ConnectionTypeAdmin(ModelView):
    def __init__(self,*args,**kwargs):
        super(ConnectionTypeAdmin,self).__init__(ConnectionType,*args,**kwargs)



with app.test_request_context():
    #admin.add_view(AccountAdmin(Account.session))
    admin.add_view(ServerAdmin(Server.session))
    admin.add_view(ConnectionTypeAdmin(ConnectionType.session))
