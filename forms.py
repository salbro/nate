from flask_wtf import Form
from wtforms.fields import TextField, TextAreaField, BooleanField, SubmitField
from wtforms import validators

from flask_wtf import Form
from wtforms.fields import TextField, PasswordField, SubmitField
from wtforms import validators
from models import User


class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    submit = SubmitField("Send")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        # if not rv:
        #     return False

        user = User(self.username.data, self.password.data)

        if not user.is_active():
            self.username.errors.append('Unknown username')
            return False

        if not user.is_authenticated():
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")
