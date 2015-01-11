from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import fields, validators,widgets
from wtforms.widgets.core import Option
#from admin.models import Type
from .fields import TagField
from flask.ext.pagedown.fields import PageDownField
from flask.ext.codemirror.fields import CodeMirrorField
from .fields import CKTextEditorField
#from blog.models import Category
from wtforms.widgets.html5 import DateInput as DateWidget
#from icons import el_icon as icons
#import admin.icons as admin_icons
#from .fields import AceEditorField
from flask import Markup
from settings import BaseConfig



#lib = BaseConfig.DEFAULT_ICON_LIBRARY
#icons = __import__('admin.icons',[],[],'icons').__dict__[lib]
#icon_fmt = '<i class="{1} {1}-{0}"></i>'
#icon_choices = {str(x):icon_fmt.format(x,lib) for x in icons}

#icons = [(icon_format.format(x,lib),x) for x,lib in icon_libs.items()]

#factory = Type.query.all()

class AddSettingForm(Form):
    name = fields.StringField('Setting Name',validators=[validators.InputRequired()])
    #type = QuerySelectField('setting type',query_factory=factory,validators=[validators.InputRequired()])
    default = fields.StringField('Default Value')
    value = fields.StringField('Setting Value')

class AddSettingTypeForm(Form):
    name = fields.StringField('Setting Type Name',validators=[validators.InputRequired()])
    widget = fields.StringField('Input Widget')

class TestForm(Form):
    title = fields.StringField('Test')
    #content = AceEditorField('content')
    submit = fields.SubmitField()

class BaseTemplateForm(Form):
    template = fields.SelectField('base template',validators=[validators.InputRequired()])#,choices=[('a','a'),('b','b'),('c','c')])

class TemplateBodyFieldForm(Form):
    name = fields.HiddenField()
    body = CKTextEditorField('body')

class TextEditorFieldForm(Form):
    content = CKTextEditorField('content')
    
class TextEditorContentForm(Form):
    content = fields.FormField(TextEditorFieldForm,label="Content",separator="_")
    submit = fields.SubmitField('save')

AddTemplateForm = TemplateBodyFieldForm


class AdminEditFileForm(Form):
    content = CKTextEditorField('content')
    file_name = fields.HiddenField()
