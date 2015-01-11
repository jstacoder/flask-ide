from wtforms import Field, widgets

class TagField(Field):
    widget = widgets.TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self,valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []
from wtforms import fields, widgets

class CKTextEditorWidget(widgets.TextArea):
    def __call__(self,field,**kwargs):
        if kwargs.get('class_',False):
            kwargs['class_'] += ' ckeditor'
        else:
            kwargs['class_'] = 'ckeditor'
        kwargs['rows'] = '8'
        return super(CKTextEditorWidget,self).__call__(field,**kwargs)

class CKTextEditorField(fields.TextAreaField):
    widget = CKTextEditorWidget()
from wtforms import fields, widgets

class CKTextEditorWidget(widgets.TextArea):
    def __call__(self,field,**kwargs):
        if kwargs.get('class_',False):
            kwargs['class_'] += ' ckeditor'
        else:
            kwargs['class_'] = 'ckeditor'
        kwargs['rows'] = '8'
        return super(CKTextEditorWidget,self).__call__(field,**kwargs)

class CKTextEditorField(fields.TextAreaField):
    widget = CKTextEditorWidget()



class CKTextEditorWidget(widgets.TextArea):
    def __call__(self,field,**kwargs):
        if kwargs.get('class_',False):
            kwargs['class_'] += ' ckeditor'
        else:
            kwargs['class_'] = 'ckeditor'
        kwargs['rows'] = '8'
        return super(CKTextEditorWidget,self).__call__(field,**kwargs)

class CKTextEditorField(fields.TextAreaField):
    widget = CKTextEditorWidget()
