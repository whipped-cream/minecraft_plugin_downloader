from logging import debug, info, error
from pathlib import Path
from re import fullmatch

from requests import get
import http_source


def get_latest_release_json(repo: str, owner: str):
    github_url = 'https://api.github.com'
    data = get(github_url + '/repos/' + owner + '/' + repo + '/releases/latest')
    # todo check status codes
    return data.json()


def download_release(response: dict, repo: str, download_path: Path, regex: str):
    info('Downloading build ' + response['tag_name'] + ' to ' + str(download_path))
    version_file_path = get_version_file_path(download_path, repo)
    debug('Creating version file at ' + str(version_file_path))
    with version_file_path.open('w') as version_file:
        debug('Writing version ' + response['tag_name'] + ' into version file')
        version_file.write(response['tag_name'] + '\n')
        assets = response['assets']
        for asset in assets:
            if regex == '' or fullmatch(regex, asset['name']):
                info('Downloading ' + asset['url'])
                http_source.__get_newest_build(download_path, asset['name'], asset['url'])
                debug('Writing ' + asset['name'] + ' into the version file')
                version_file.write(asset['name'])


def download_build_if_newer(response: dict, repo: str, download_path: Path, regex: str):
    version_file_path = get_version_file_path(download_path, repo)
    if version_file_path.is_file():
        with version_file_path.open() as f:
            line = f.readline()
            local_version = line.strip('\n')
            remote_version = response['tag_name']
            if remote_version != local_version:
                info('Local version ' + local_version + ' != remote version ' + remote_version
                     + '. Proceeding to download')
                old_file = f.readline()
                if old_file != '':
                    old_file_path = download_path.joinpath(old_file)
                    debug('Deleting old file ' + str(old_file_path))
                    old_file_path.unlink(True)
            else:
                info('Local version ' + local_version + ' == remote version ' + remote_version
                     + '. Not downloading')
                return
        debug('Deleting version file ' + str(version_file_path))
        version_file_path.unlink()
    else:
        info('No version file found. Proceeding as if new')
    download_release(response, repo, download_path, regex)


def get_download_path(download_dir: str):
    download_path = Path(download_dir)
    if not download_path.exists():
        raise FileNotFoundError
    return download_path


def get_version_file_path(download_path: Path, repo: str):
    return download_path.joinpath(repo + '.version')


def get_newest_build(download_dir: str, owner: str, repo: str, regex: str = ''):
    response = get_latest_release_json(repo, owner)
    download_path = get_download_path(download_dir)
    download_build_if_newer(response, repo, download_path, regex)
