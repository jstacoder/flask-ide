from wtforms import Field, widgets
from htmlbuilder import html


class AceWidget(object):
    _cdn = 'https://cdnjs.cloudflare.com/ajax/libs/ace/1.1.3/ace.js'
    _js = '''
    var editor = ace.edit("{}");
    editor.setOption('mode','ace/mode/{}');
    editor.setTheme('ace/theme/{}');
    '''

    def __call__(self,field,*args,**kwargs):
        js = html.div()(
                html.div(id=field.id,height="400px")(),
                html.script(
                    src = self._cdn
                )(),
                html.script()(
                    self._js.format(
                       field.id,
                        field._mode,
                        field._theme,
                    )
                )            
            )
        return html.div(id=field.id)(js)


class AceField(Field):
    _mode = 'python'
    _theme = 'twilight'

    def __init__(self,*args,**kwargs):
        if 'mode' in kwargs:
            self._mode = kwargs.pop("mode")
        if 'theme' in kwargs:
            self._theme = kwargs.pop("theme")
            kwargs['widget'] = AceWidget()
        super(AceField,self).__init__(*args,**kwargs) 

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
