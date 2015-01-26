from flask_xxl.basemodels import BaseMixin
import sqlalchemy.orm as orm
import sqlalchemy as db

class File:
    __table_args__ = {'abstract':True}
    __abstract__ = True

    name = db.Column(db.String(255),nullable=False)
    parent_id = db.Column(db.Integer,db.ForeignKey('directories.id'))
    parent = orm.relationship('Directory',backref=orm.backref(
                        'files',lazy='dynamic'))
    full_path = db.Column(db.String(255),nullable=False,unique=True)



class Directory(BaseMixin):

    name = db.Column(db.String(255),nullable=False)
    full_path = db.Column(db.String(255),nullable=False,unique=True)


class TemplateFile(File,BaseMixin):
    pass

class CodeFile(File,BaseMixin):
    pass
