import configparser
from pathlib import Path

from app.provider.file import FileProvider


class ConfigProvider:
    def __init__(self, path: Path) -> None:
        file = FileProvider(path=path)
        config = configparser.ConfigParser()
        config.read(file.payload)

        self.payload = config