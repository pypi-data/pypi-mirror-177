from pathlib import Path
from pydantic import BaseSettings, DirectoryPath

BASEPATH = Path(".") / "gdshoplib"


class Settings(BaseSettings):
    TEMPLATES_PATH: DirectoryPath = (BASEPATH / "templates").resolve()


settings = Settings()
