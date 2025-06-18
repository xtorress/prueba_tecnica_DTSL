import bcrypt

def get_password_hashed(pswd: str):
    byte_pswd = pswd.encode('utf-8')
    hashed = bcrypt.hashpw(byte_pswd, bcrypt.gensalt())
    return hashed.decode('utf-8')