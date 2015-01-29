"""A collection of utility functions."""

import json
from os import path

import click
from docker.client import Client
from docker.utils import kwargs_from_env

_LOG_LEVEL = 0
LOG_PREFIXES = {
    0: click.style('>', fg='white', bold=True),
    1: click.style('>>', fg='cyan', bold=True),
    2: click.style('>>>', fg='blue', bold=True),
}
_DOCKER_CLIENT = None


def set_log_level(log_level):
    """Set the log level to use.

    Log levels are provided as an integer, and the following levels are available:
    0: The default log level
    1: Info level logging
    2: Debug level logging
    """
    if log_level not in [0, 1, 2]:
        return False

    global _LOG_LEVEL  # pylint: disable = global-statement
    _LOG_LEVEL = log_level
    return True


def get_log_level():
    """Get the current log level."""
    return _LOG_LEVEL


def _print(message, log_level, prefix, **kwargs):
    """Print a message to the console, depending on log level."""
    if log_level <= get_log_level():
        if prefix:
            click.secho('{} '.format(LOG_PREFIXES[log_level]), nl=False)

        return click.secho(message, **kwargs)


def log(message, prefix=True, **kwargs):
    """Print a default level log message."""
    return _print(message, log_level=0, prefix=prefix, **kwargs)


def info(message, prefix=True, **kwargs):
    """Print an info level log message."""
    return _print(message, log_level=1, prefix=prefix, **kwargs)


def debug(message, prefix=True, **kwargs):
    """Print a debug level log message."""
    return _print(message, log_level=2, prefix=prefix, **kwargs)


def docker_client():
    """Create a Docker client instance or return an existing one."""
    global _DOCKER_CLIENT  # pylint: disable = global-statement

    if _DOCKER_CLIENT:
        return _DOCKER_CLIENT
    else:
        # assert_hostname=False is required when using boot2docker, it's taken as a hint from Fig: https://github.com/docker/fig/blob/master/compose/cli/docker_client.py#L29
        _DOCKER_CLIENT = Client(**kwargs_from_env(assert_hostname=False))
        return _DOCKER_CLIENT


def pull_image(wanted_image):
    """Download Docker image if it isn't already local."""
    if ':' not in wanted_image:
        wanted_image = '{}:latest'.format(wanted_image)

    debug('Checking if "{}" is among the local images in Docker.'.format(wanted_image))
    for image in docker_client().images(name=wanted_image.split(':')[0]):
        if wanted_image in image['RepoTags']:
            info('Docker image found.')
            return True

    log('The Docker image "{}" was not found locally, pulling it: '.format(wanted_image), nl=False)
    for data in docker_client().pull(wanted_image, stream=True):
        data = data.decode('utf-8')
        line = json.loads(data)
        if not line.get('error'):
            continue

        log('Failed! Error message follows:', fg='red', bold=True, prefix=False)
        log('  {}'.format(line['error']), err=True, prefix=False)
        return False

    log('Done.', fg='green', prefix=False)
    return True


def convert_volumes_list(volumes):
    """Turn a dict into a list of volumes and binds in the format Docker loves."""
    volume_list = []
    binds = dict()
    for local, container in volumes.items():
        volume_list.append(container)
        binds[path.abspath(local)] = container
    return volume_list, binds
