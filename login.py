from flask_wtf import Form
from wtforms.fields import TextField, PasswordField, SubmitField
from wtforms import validators
from users import User


class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    submit = SubmitField("Send")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User(username, password)

        if not user.is_active():
            self.username.errors.append('Unknown username')
            return False

        if not user.is_authenticated():
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True
