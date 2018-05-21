from models.user import UserModel

def authenticate(username, password):
    u = UserModel.find_by_username(username)
    if u and u.password==password:
        return u

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)