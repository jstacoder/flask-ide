from jinja2 import Environment
from flask import jsonify,request,flash
from flask.json import loads
from flask.views import MethodView
import os.path as op


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
        with open(file_name,'w') as f:
            f.write(content)
        success = op.isfile(file_name) and\
                open(file_name,'r').read() == content
        if success:
            flash(self._SUCCESS_MESSAGE.format(file_name),'success')
        else:
            flash(self._ERROR_MESSAGE.format(file_name),'danger')
        return jsonify(dict(success=success,continue_edit=bool(continue_edit)))
