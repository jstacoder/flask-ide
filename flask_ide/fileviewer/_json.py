from jinja2 import Environment
from flask import jsonify,request,flash
from flask.json import loads
from flask.views import MethodView
import os.path as op
from ssh_client import login
from flask import current_app

class LoginView(MethodView):

    def post(self):
        conn = login(**request.form)
        return jsonify(data=conn)
                
def save_file(name,content):
    if not current_app.config.get('FILEVIEWER_READONLY'):
        with open(name,'w') as f:
            f.write(content)
    return (op.isfile(name) and open(name,'r').read() == content) if not current_app.config.get('FILEVIEWER_READONLY') else True


class JsonFileView(MethodView):
  
  def get(self,file_name):
    if op.isfile(op.abspath(file_name)):
        data = open(file_name,'r').read()
        template_str = '{% highlight "python" %}{{ content }}{% endhighlight %}'
        jinja_env = Environment(extensions=['jinja2_highlight.HighlightExtension'])
        template = jinja_env.from_string(template_str)
        return jsonify(dict(content=template.render(content=data)))
    return jsonify(dict(error=1))

class JsonCodeView(MethodView):
    _SUCCESS_MESSAGE = 'You saved {}'
    _ERROR_MESSAGE = 'Error saving {}'

    def get(self):
        content = request.args.get('content',None)
        file_name = request.args.get('file_name',None)
        continue_edit = int(request.args.get('continue_edit',0))
        success = save_file(file_name,content)
        if success:
            flash(self._SUCCESS_MESSAGE.format(file_name),'success')
        else:
            flash(self._ERROR_MESSAGE.format(file_name),'danger')
        return jsonify(dict(success=success,continue_edit=bool(continue_edit)))

    def post(self):
        file_name = request.args.get('file_name',None)
        content = request.form.get('content',None)
        continue_edit = request.form.get('continue_edit',None)
        success = save_file(file_name,content)
        if success:
            flash(self._SUCCESS_MESSAGE.format(file_name),'success')
        else:
            flash(self._ERROR_MESSAGE.format(file_name),'danger')
        return jsonify(dict(success=success,continue_edit=bool(continue_edit)))


