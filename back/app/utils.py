import bcrypt

def get_password_hashed(pswd: str):
    byte_pswd = pswd.encode('utf-8')
    return bcrypt.hashpw(byte_pswd, bcrypt.gensalt())