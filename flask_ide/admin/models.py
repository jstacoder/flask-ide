from main.basemodels import BaseMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declared_attr
from LoginUtils import check_password, encrypt_password
from ext import db

#for attr in dir(db):
#    globals()[attr] = getattr(db,attr)
Text,Boolean,Model,Column,Integer,String,relationship,backref,ForeignKey = db.Text,db.Boolean,db.Model,db.Column,db.Integer,db.String,db.relationship,db.backref,db.ForeignKey
'''
class BackendSetting(BaseMixin,Model):
    __tablename__ = 'backend_settings'
    __table_args__ = {'extend_existing':True}

    name = Column(String(255),nullable=False,unique=True)
    setting_type_id = Column(Integer,ForeignKey('setting_types.id'))
    setting_type = relationship('SettingType',backref=backref(
        'backend_settings',lazy='dynamic'))
    default = Column(String(255))
    value = Column(String(255))

    setting_group = relationship('SettingGroup',backref=backref(
        'settings',lazy='dynamic'))
    setting_group_id = Column(Integer,ForeignKey('setting_groups.id'))

    @declared_attr
    def __table_args__(cls):
        return (UniqueConstraint('name','setting_group_id'),{})

    @property
    def widget(self):
        if self.type:
            return self.type.widgets
        else:
            return ''

class SettingType(BaseMixin,Model):
    __tablename__ = 'setting_types'

    name = Column(String(255),nullable=False)
    widgets = relationship('Widget',backref=backref(
        'type'),lazy='dynamic')
    field_type = Column(String(255))
    required = Column(Boolean,default=False)
    data_type = Column(String(255))

    def __repr__(self):
        return '{} {}'.format(self.name,self.data_type)
'''
class Widget(BaseMixin,Model):
    __tablename__ = 'widgets'

    name = Column(String(255),nullable=False)
    label = Column(String(255))
    content = Column(Text,nullable=False)
    type_id = Column(Integer,ForeignKey('setting_types.id'))

    def __repr__(self):
        return self.name

class SettingGroup(BaseMixin,Model):
    __tablename__ = 'setting_groups'

    title = Column(String(255),nullable=False)
    app = Column(String(255))


    

class AdminTab(BaseMixin,Model):
    __tablename__ = 'admin_tabs'

    name = Column(String(255),nullable=False)
    tab_id = Column(String(50),nullable=False)
    tab_title = Column(String(255))
    content = Column(Text)

    def __str__(self):
        return self.content or ''

    @staticmethod
    def get_tab_links():
        rtn = []
        for panel in AdminTab.query.all():
            rtn.append((panel.name,panel.tab_id))
        return rtn
    
    
class FontIcon(BaseMixin,Model):
    __tablename__ = 'font_icons'

    name = Column(String(255),nullable=False)
    library_id = Column(Integer,ForeignKey('font_icon_librarys.id'))
    library = relationship('FontIconLibrary',backref=backref(
                'font_icons',lazy='dynamic'))

    #__table_args__ = (UniqueConstraint(library,name,name='_library_font_icon'),)
    
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return '<span class="{0} {0}-{1}"></span>'.format(self.library.name,self.name)





class FontIconLibrary(BaseMixin,Model):
    __tablename__ = 'font_icon_librarys'

    @declared_attr
    def __table_args__(cls):
        return (UniqueConstraint('name','call_string'),{})

    name = Column(String(255),unique=True)
    call_string = Column(String(255),unique=True)

    def __str__(self):
        return self.call_string or self.name

    def __repr__(self):
        return str(self)

    





    
