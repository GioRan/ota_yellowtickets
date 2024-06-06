from pathlib import Path


class FileProvider:
    def __init__(self, path: Path) -> None:
        if path.exists() is False and path.is_file() is False:
            raise ValueError(f'Invalid file path -> {path}')

        self.payload = path.absolute().as_posix()