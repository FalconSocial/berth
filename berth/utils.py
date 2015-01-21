"""A collection of utility functions."""

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
        debug('Reusing existing Docker client.')
        return _DOCKER_CLIENT
    else:
        debug('Creating Docker client.')
        _DOCKER_CLIENT = Client(**kwargs_from_env())
        return _DOCKER_CLIENT
