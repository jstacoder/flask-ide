#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~
"""
import os
import sys
import subprocess
import unittest
from flask_xxl.basemodels import BaseMixin as Model
from flask import url_for
from flask.ext.script import Shell, Manager, prompt_bool
from flask.ext.script.commands import Clean,ShowUrls
if os.environ.get('TESTING',False):
    from testing import TC
    app = TC().create_app()
else:
    from app import app

import urllib
import sqlalchemy_utils as squ
from flask.ext.alembic.cli.script import manager as alembic_manager
from auth.models import User
manager = Manager(app)



import os.path as op
 

@manager.command
def show_templates():
    print '\n'.join(sorted(app.jinja_env.list_templates()))

@manager.command
def gather_template_files(verbose=True):
    template_files = map(lambda x: (
        x[0],
        x[1],
        open(x[0],'r').read()
        ),map(lambda x: (
            x.filename,
            x.name
            ),map(
                app.jinja_env.get_template,
                app.jinja_env.list_templates()
                )
            )
        )
    base = 'templates'
    success = True
    for location,name,text in template_files:
        filename = op.join(base,name)
        filedir = op.join(base,op.dirname(name))
        if not op.exists(filedir):
            if verbose:
                print 'Directory path {} does not exist, creating now...\n\n'.format(filedir)
            os.makedirs(filedir)
            with open(filename,'w') as f:
                try:
                    if verbose:
                        print 'Preparing to write file {}\n'.format(filename)
                    f.write(text)
                    if verbose:
                        print 'wrote {} to file\n'.format(filename)
                except:
                    success = False
                    pass
    return success
                
                
                

sys.path.insert(0,os.path.join(os.path.dirname(__file__),'venv','lib','python2.7','site-packages'))
print sys.path[0]



def get_meta():
    from flask_ide.core import models
    engine = Model._engine
    meta = Model.metadata
    #engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    engine.echo = True
    meta.bind = engine
    return meta

@manager.command
def drop_db():
    get_meta().drop_all()

@manager.command
def create_db():
    from auth.models import User
    from core.models import Account,ConnectionType,Server
    get_meta().create_all()

@manager.command
def seed_db():
    from core.models import Account,Server,ConnectionType
    local_c = ConnectionType(name='local',connection_class='local')
    local_c.save()
    local = Server(ip_address='127.0.0.1',name='localhost',connection_type_id=local_c.id)    
    local.save()
    act = Account(username='local',password='local',base_dir='/',server_id=local.id)
    act.save()


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def show_models():
    for table in Model.metadata.tables:
        print table

@manager.command
def show_routes():
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "<{0}>".format(arg)
        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint,**options)
        line = urllib.unquote("{:30s} {:20s} {}".format(rule.endpoint,methods,url))
        output.append(line)
    for line in sorted(output):
        print line

@manager.command
def init_data():
    if prompt_bool('Do you want to kill your db?'):
        if squ.database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            squ.drop_database(app.config['SQLALCHEMY_DATABASE_URI'])
    try:
        drop_db()
    except:
        pass
    try:
        squ.create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        create_db()
    except:
        pass
    seed_db()
    user = User().query.filter(User.email=='kyle@level2designs.com').first()
    if user is None:
       user = User(username='kyle', email='kyle@level2designs.com', password='14wp88')
    user.save()

class DB(object):
    Model = Model
    metadata = Model.metadata
    sq = squ
    app.test_request_context().push()
    engine = Model._engine



if __name__ == '__main__':
    manager.add_command('clean',Clean())
    manager.add_command('urls',ShowUrls())
    manager.add_command('db',alembic_manager)
    app.test_request_context().push()
    conn = Model._engine.raw_connection()
    conn.connection.text_factory = str
    manager.add_command('shell', Shell(make_context=lambda:{'app': app, 'db': DB()}))
    app.extensions = app.extensions or {} 
    class O(object):
        pass
    db = O()
    db.db = DB()
    app.extensions['sqlalchemy'] = db
    manager.run()
