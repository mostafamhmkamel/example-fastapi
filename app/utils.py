from passlib.context import CryptContext #important for hashing passwords

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto' ) #basically stating what hashing algorithm we want to use

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) 

#to get environment variables (which are used to avoid hardcoding passwords and urls in our system)
# we import os
# write path = os.getenv("name of environment variable")
# print(path)