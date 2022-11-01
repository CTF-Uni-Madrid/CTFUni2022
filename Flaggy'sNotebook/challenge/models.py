from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

    def set_password(self, password):
        self.password = password

    def set_id(self, id):
        self.id = id
            
    def __repr__(self):
        return '<User {}>'.format(self.id)

    def is_authenticated(self):
        return True
    
    def get_id(self):         
        return str(self.id)