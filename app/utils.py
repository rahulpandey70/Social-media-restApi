from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hashed Password
def hashPassword(password: str):
    return pwd_context.hash(password)


def verifyPassword(plainPass, hashedPass):
    return pwd_context.verify(plainPass, hashedPass)
