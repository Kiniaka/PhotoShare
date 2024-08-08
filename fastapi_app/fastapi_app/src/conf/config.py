from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    """
    Configuration settings for the application, loaded from environment variables.

    Attributes:
        sqlalchemy_database_url (str): The database connection URL.
        secret_key (str): The secret key for JWT token generation.
        algorithm (str): The algorithm used for JWT token encoding. Defaults to "HS256".
        mail_username (str): The username for the mail server.
        mail_password (str): The password for the mail server.
        mail_from (str): The email address to use for sending emails.
        mail_port (str): The port to use for the mail server.
        mail_server (str): The address of the mail server.
        redis_host (str): The host address for the Redis server.
        redis_port (str): The port for the Redis server.
        redis_password (str, optional): The password for the Redis server, if any.
        cloudinary_name (str): The Cloudinary cloud name.
        cloudinary_api_key (str): The Cloudinary API key.
        cloudinary_api_secret (str): The Cloudinary API secret.

    Config:
        env_file (str): The name of the file to load environment variables from.
        env_file_encoding (str): The encoding of the environment file.
    """
    sqlalchemy_database_url: str = os.getenv('DATABASE_URL')
    secret_key: str = os.getenv('SECRET_KEY')
    algorithm: str = "HS256"
    mail_username: str = os.getenv('MAIL_USERNAME')
    mail_password: str = os.getenv('MAIL_PASSWORD')
    mail_from: str = os.getenv('MAIL_FROM')
    mail_port: str = os.getenv('MAIL_PORT')
    mail_server: str = os.getenv('MAIL_SERVER')
    redis_host: str = os.getenv('REDIS_HOST')
    redis_port: str = os.getenv('REDIS_PORT')
    redis_password: str = os.getenv('REDIS_PASSWORD', None)
    cloudinary_name: str = os.getenv('CLOUDINARY_CLOUD_NAME')
    cloudinary_api_key: str = os.getenv('CLOUDINARY_API_KEY')
    cloudinary_api_secret: str = os.getenv('CLOUDINARY_API_SECRET')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
