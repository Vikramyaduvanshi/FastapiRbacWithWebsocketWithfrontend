import bcrypt


def hashpassword(password:str):
    inbytes= password.encode("utf-8")
    salt= bcrypt.gensalt()
    hashed_password= bcrypt.hashpw(inbytes,salt)
    return hashed_password.decode("utf-8")

def verifypassword(plain_password: str, hashed_password_from_db: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), 
        hashed_password_from_db.encode("utf-8")
    )