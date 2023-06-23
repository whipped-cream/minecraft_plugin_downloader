from logging import debug, info, error
from pathlib import Path
from re import fullmatch

from jenkinsapi.build import Build
from jenkinsapi.jenkins import Jenkins


def get_anonymous_server_instance(jenkins_url: str):
    info('Getting an anonymous Jenkins instance at ' + jenkins_url)
    return Jenkins(jenkins_url)


def get_last_successful_build(jenkins: Jenkins, job_name: str):
    info('Getting the last successful build of ' + job_name)
    if not jenkins.has_job(job_name):
        error('Job does not exist!')
        raise LookupError
    else:
        job = jenkins.get_job(job_name)
        last_successful_build = job.get_last_good_build()
        info('Got last successful build as ' + str(last_successful_build.get_number()))
        return last_successful_build


def download_build(build: Build, download_path: Path, regex: str):
    info('Downloading build ' + str(build.get_number()) + ' to ' + str(download_path))
    version_file_path = get_version_file_path(download_path, build)
    debug('Creating version file at ' + str(version_file_path))
    with version_file_path.open('w') as version_file:
        debug('Writing version ' + str(build.get_number()) + ' into version file')
        version_file.write(str(build.get_number()) + '\n')
        artifacts = build.get_artifacts()
        for artifact in artifacts:
            if regex == '' or fullmatch(regex, artifact.url):
                info('Downloading ' + artifact.url)
                artifact.save_to_dir(str(download_path))
                debug('Writing ' + artifact.filename + ' into the version file')
                version_file.write(artifact.filename)


def download_build_if_newer(build: Build, download_path: Path, regex: str):
    version_file_path = get_version_file_path(download_path, build)
    if version_file_path.is_file():
        with version_file_path.open() as f:
            line = f.readline()
            local_version = int(line)
            remote_version = int(build.get_number())
            if remote_version > local_version:
                info('Local version ' + str(local_version) + ' <= remote version ' + str(remote_version)
                     + '. Proceeding to download')
                old_file = f.readline()
                if old_file != '':
                    old_file_path = download_path.joinpath(old_file)
                    debug('Deleting old file ' + str(old_file_path))
                    old_file_path.unlink(True)
            else:
                info('Local version ' + str(local_version) + ' >= remote version ' + str(remote_version)
                     + '. Not downloading')
                return
        debug('Deleting version file ' + str(version_file_path))
        version_file_path.unlink()
    else:
        info('No version file found. Proceeding as if new')
    download_build(build, download_path, regex)


def get_download_path(download_dir: str):
    download_path = Path(download_dir)
    if not download_path.exists():
        raise FileNotFoundError
    return download_path


def get_version_file_path(download_path: Path, build: Build):
    return download_path.joinpath(str(build.job) + '.version')


def get_newest_build(download_dir: str, jenkins_url: str, job_name: str, regex: str = ''):
    jenkins = get_anonymous_server_instance(jenkins_url)
    last_successful_build = get_last_successful_build(jenkins, job_name)
    download_path = get_download_path(download_dir)
    download_build_if_newer(last_successful_build, download_path, regex)