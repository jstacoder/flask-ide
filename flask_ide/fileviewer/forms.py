from flask.ext.codemirror.fields import CodeMirrorField
from wtforms import fields,widgets
from flask.ext.wtf import Form
from codemirror_modes import themes, modes


theme_choice = {x.lower():x for x in themes}.items()
mode_choice = {x.lower():x for x in modes}.items()
test_choice = [('x','x'),('y','y'),('z','z')]
class CodeForm(Form):
    content = CodeMirrorField('content')
    file_name = fields.HiddenField('file_name')
    submit = fields.SubmitField('submit')
    theme = fields.SelectField('Theme',choices=theme_choice)
    mode = fields.SelectField('mode',choices=mode_choice)
    test_select = fields.SelectField('test',choices=test_choice,
                                        option_widget=widgets.RadioInput(),
                                        widget=widgets.ListWidget(prefix_label=False))