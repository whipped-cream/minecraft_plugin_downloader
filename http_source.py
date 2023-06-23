from pathlib import Path

import requests


def get_download_path(download_dir: str):
    download_path = Path(download_dir)
    if not download_path.exists():
        raise FileNotFoundError
    return download_path


def __get_newest_build(download_path: Path, name: str, url: str):
    download_path = download_path / name
    data = requests.get(url)
    download_path.open('wb').write(data.content)


def get_newest_build(download_dir: str, name: str, url: str):
    download_path = get_download_path(download_dir)
    __get_newest_build(download_path, name, url)

