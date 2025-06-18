import bcrypt

def get_password_hashed(pswd: str):
    byte_pswd = pswd.encode('utf-8')
    hashed = bcrypt.hashpw(byte_pswd, bcrypt.gensalt())
    return hashed.decode('utf-8')

def check_password(pswd: str, pswd_db: str):
    byte_pswd = pswd.encode('utf-8')
    byte_pswd_db = pswd_db.encode('utf-8')
    return bcrypt.checkpw(byte_pswd, byte_pswd_db)