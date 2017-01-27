CREDS = "creds.json"
import json

class User():

    def __init__(self, username, password):
        self.username = username
        self.password = password


    def get_password(self, cred_dict, username):
        return cred_dict[username]['password']

    def is_authenticated(self):
        '''
        This property should return True if the user is authenticated, i.e. they have provided valid credentials. (Only authenticated users will fulfill the criteria of login_required.)
        '''
        with open(CREDS, "r") as fp:
            credentials = json.load(fp)

        print("authenticated in user: " + str( self.get_password(credentials, self.email) == self.password))
        return self.get_password(credentials, self.email) == self.password


    def is_active(self):
        '''
        This property should return True if this is an active user - in addition to being authenticated, they also have activated their account, not been suspended, or any condition your application has for rejecting an account. Inactive accounts may not log in (without being forced of course).
        '''
        with open(CREDS, "r") as fp:
            d = json.load(fp)
            print("is_active says keys are: " + str(d.keys()))
            return self.email in list(d.keys())

    def is_anonymous(self):
        '''
        This property should return True if this is an anonymous user. (Actual users should return False instead.)
        '''
        with open(CREDS, "r") as fp:
            return self.email not in json.load(fp).keys()


    def get_id(self):
        '''
        This method must return a unicode that uniquely identifies this user, and can be used to load the user from the user_loader callback. Note that this must be a unicode - if the ID is natively an int or some other type, you will need to convert it to unicode.
        '''
        with open(CREDS, "r") as fp:
            return json.load(fp)[self.email]['id']

def userBased_to_idBased(cred_dict):
    to_return = {}
    for (email, info_dict) in cred_dict.items():
        to_return[info_dict['id']] = {'email': email, 'password': info_dict['password']}
    return to_return

def get_user_object(user_id):
    with open(CREDS, "r") as fp:
        id_dict = userBased_to_idBased(json.load(fp))
    return User(id_dict[user_id]['email'], id_dict[user_id]['password'])
