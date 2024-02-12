from pydantic_settings import BaseSettings

# the below will look for the below variables in your system's environment variables
# usually, instead of storing default values, you would have it in your system or another python file outside the directory

class Settings(BaseSettings):
    database_hostname: str
    database_port:str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    #connecting the above variables to our environment variables file

    class Config:
        env_file = 'app/.env'


settings = Settings() # creating instance of the above class
