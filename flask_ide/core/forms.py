from wtforms import Form, fields, validators


class AddSSHServerAccountForm(Form):
    username = fields.StringField('Account User',validators=[validators.InputRequired()])
    base_dir = fields.StringField('Base directory',validators=[validators.InputRequired()])
    password = fields.PasswordField('Account Password',validators=[validators.InputRequired()])
    confirm = fields.PasswordField('Confirm password',validators=[validators.InputRequired(),validators.EqualTo('password')])
    server_id_num = fields.HiddenField()


class AddSSHServerForm(Form):
    host = fields.StringField('Host',validators=[validators.InputRequired()])
    server_name = fields.StringField('Name For Server',validators=[validators.InputRequired()])
    accounts = fields.FieldList(fields.FormField(AddSSHServerAccountForm),min_entries=1)
    submit = fields.SubmitField()
