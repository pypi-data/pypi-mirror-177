from pydantic import BaseSettings


class Settings(BaseSettings):
    NOTION_SECRET_TOKEN: str
    PRODUCT_DB: str = "2d1707fb-877d-4d83-8ae6-3c3d00ff5091"
