from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    open_route_api_key: str

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
