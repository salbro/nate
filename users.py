CREDS = "creds.json"
import json
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    password = Column(String(20))
    registered_on = Column('registered_on', DateTime)

    def __init__(self, _name, _password):
        self.name = _name
        self.password = _password
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return "<User(name='%s', password='%s')>" % (
                                self.name, self.password)

    def get_password(self):
        usr = User.query.filter(User.name==self.name).first()
        return usr.password if usr else None

    def is_authenticated(self):
        '''
        This property should return True if the user is authenticated, i.e. they have provided valid credentials. (Only authenticated users will fulfill the criteria of login_required.)
        '''
        usr = User.query.filter(User.name==self.name, User.password==self.password).first()
        return (usr is not None)

    def is_active(self):
        '''
        This property should return True if this is an active user - in addition to being authenticated, they also have activated their account, not been suspended, or any condition your application has for rejecting an account. Inactive accounts may not log in (without being forced of course).
        '''
        return True

    def is_anonymous(self):
        '''
        This property should return True if this is an anonymous user. (Actual users should return False instead.)
        '''
        return False

    def get_id(self):
        '''
        This method must return a unicode that uniquely identifies this user, and can be used to load the user from the user_loader callback. Note that this must be a unicode - if the ID is natively an int or some other type, you will need to convert it to unicode.
        '''
        usr = User.query.filter(User.name==self.name, User.password==self.password).first()
        return usr.id if usr else None





# def userBased_to_idBased(cred_dict):
#     to_return = {}
#     for (email, info_dict) in cred_dict.items():
#         to_return[info_dict['id']] = {'email': email, 'password': info_dict['password']}
#     return to_return
#
# def get_user_object(user_id):
#     with open(CREDS, "r") as fp:
#         id_dict = userBased_to_idBased(json.load(fp))
#     return User(id_dict[user_id]['email'], id_dict[user_id]['password'])
