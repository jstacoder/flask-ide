from flask_ide import app,core

with app.app_context():
    cls = core.models.ConnectionRecord
    print '\n'.join(map(str,[x.ip_address for x in cls.query.all()]))
