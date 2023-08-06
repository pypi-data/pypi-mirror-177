import os
from pathlib import Path

from pydantic import BaseSettings, DirectoryPath

BASEPATH = Path(os.path.dirname(os.path.realpath(__file__))).parent


class Settings(BaseSettings):
    TEMPLATES_PATH: DirectoryPath = (BASEPATH / "templates").resolve()


settings = Settings()
