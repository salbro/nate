from flask_wtf import Form
from wtforms.fields import TextField, TextAreaField, BooleanField, SubmitField, PasswordField
from wtforms import validators

from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from tfy_db_credentials import tfy_db_url

# from database import SessionMaker
Base = declarative_base()

class User(Base):
    __tablename__ = 'devusers'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    password = Column(String(20))
    registered_on = Column('registered_on', DateTime)

    def __init__(self, _name, _password):
        self.name = _name
        self.password = _password
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return "<User(name=%s, password=%s)>" % (
                                self.name, self.password)

    def is_authenticated(self):
        '''
        This property should return True if the user is authenticated, i.e. they have provided valid credentials. (Only authenticated users will fulfill the criteria of login_required.)
        '''
        engine = create_engine(tfy_db_url, convert_unicode=True)
        SessionMaker = sessionmaker(bind=engine)
        session = SessionMaker()
        usr = session.query(User).filter(User.name==self.name, User.password==self.password).first()
        session.close()
        engine.dispose()
        return (usr is not None)
        # usr = User.query.filter(User.name==self.name, User.password==self.password).first()
        # return (usr is not None)

    def is_active(self):
        '''
        This property should return True if this is an active user - in addition to being authenticated, they also have activated their account, not been suspended, or any condition your application has for rejecting an account. Inactive accounts may not log in (without being forced of course).
        '''
        engine = create_engine(tfy_db_url, convert_unicode=True)
        SessionMaker = sessionmaker(bind=engine)
        session = SessionMaker()
        usr = session.query(User).filter(User.name==self.name).first()
        session.close()
        engine.dispose()
        return (usr is not None)

    def is_anonymous(self):
        '''
        This property should return True if this is an anonymous user. (Actual users should return False instead.)
        '''
        return False

    def get_id(self):
        '''
        This method must return a unicode that uniquely identifies this user, and can be used to load the user from the user_loader callback. Note that this must be a unicode - if the ID is natively an int or some other type, you will need to convert it to unicode.
        '''

        engine = create_engine(tfy_db_url, convert_unicode=True)
        SessionMaker = sessionmaker(bind=engine)
        session = SessionMaker()
        usr = session.query(User).filter(User.name==self.name, User.password==self.password).first()
        session.close()
        engine.dispose()
        return usr.id if usr else None


class LoginForm(Form):
    username = TextField('Username', [validators.Required()], render_kw={"placeholder": "Username (email)"}) #render_kw={"placeholder": "Username (email)"}
    password = PasswordField('Password', [validators.Required()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Log In")

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



class Question(Base):
    __tablename__ = 'devquestions'
    q_id = Column(Integer, Sequence('question_id_seq'), primary_key=True)
    q_category = Column(String(50))
    q_text = Column(String(300))
    n_upvotes = Column(Integer)
    n_downvotes = Column(Integer)
    registered_on = Column('registered_on', DateTime)

    def __init__(self, q_category, q_text, n_upvotes=0, n_downvotes=0):
        self.q_category = q_category
        self.q_text = q_text
        self.n_upvotes = n_upvotes
        self.n_downvotes = n_downvotes
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return "<Question(id=%s, category=%s, text=%s, %s upvotes, %s downvotes, created %s)>" % (
                                self.q_id, self.q_category, self.q_text, self.n_upvotes, self.n_downvotes, self.registered_on)

    def upvote(self):
        self.n_upvotes += 1

    def downvote(self):
        self.n_downvotes += 1


class Vote(Base):
    __tablename__ = 'devvotelog'
    vote_id = Column(Integer, Sequence('vote_id_seq'), primary_key=True)
    question_id = Column(Integer)
    vote_direction = Column(String(4)) # "up" or "down" ... mySQL does not support check constraints
    user_id = Column(Integer)
    registered_on = Column('registered_on', DateTime)

    def __init__(self, question_id, vote_direction, user_id):
        self.question_id = question_id
        self.vote_direction = vote_direction
        self.user_id = user_id
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return "<Vote(user_id %s %svoted question_id %s at %s)>" % (
                                self.user_id, self.vote_direction, self.question_id, self.registered_on)

    # returns True if this user has voted on this question before
    def user_is_double_voting(self):
        vote = Vote.query.filter(Vote.user_id==self.user_id, Vote.question_id==self.question_id).first()
        return (vote is not None)
