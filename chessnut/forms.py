from wtforms import Form, TextField, TextAreaField, PasswordField, validators

strip_filter = lambda x: x.strip() if x else None


class CreateUser(Form):
    name = TextField('Username', [validators.Length(min=1, max=255)],
                     filters=[strip_filter])
    email = TextField('Email Address', [validators.Email()],
                      filters=[strip_filter])
    password = PasswordField('Password', [validators.Length(min=4, max=255)],
                             filters=[strip_filter])
