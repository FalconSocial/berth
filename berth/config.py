"""Verifies the configuration provided."""

from os import mkdir, path

import berth.utils as utils
import yaml
import yaml.parser


def read(file_pointer):
    """Read the configuration file and parse the YAML contents."""
    utils.debug('Reading the configuration file.')

    try:
        config = yaml.load(file_pointer.read())
    except yaml.parser.ParserError as error:
        utils.log('The configuration file could not be parsed:', err=True, fg='red', bold=True)
        utils.log(error.context, err=True, prefix=False)
        utils.log(str(error.context_mark), err=True, prefix=False)
        utils.log(error.problem, err=True, prefix=False)
        utils.log(str(error.problem_mark), err=True, prefix=False)
        return False

    utils.info('The configuration file "{}" has been parsed.'.format(file_pointer.name))
    utils.debug('Parsed configuration:\n{}'.format(config))
    return config


def verify(config):
    """Verify the configuration contain the necessary details."""
    errors = []

    required = {
        'build': {
            'image',
            'script',
        },
        'package': {
            'volumes',
            'fpm',
        },
    }

    for section, fields in required.items():
        if section not in config:
            errors.append('A "{}" section is missing.'.format(section))
        elif not isinstance(config[section], dict):
            errors.append('The "{}" section has to be a dictionary.'.format(section))
        else:
            for field in fields:
                if field not in config[section]:
                    errors.append('"{}" is required in the {} section.'.format(field, section))

    if not errors:
        for section in required.keys():
            for local_path, container_path in config.get(section, dict()).get('volumes', dict()).items():
                if not path.exists(local_path) and not create_local_directory(local_path):
                    errors.append('The path "{}" specified as a {} volume does not exist on the local machine.'.format(local_path, section))
                if not path.isabs(container_path):
                    errors.append('The path "{}" specified as a {} volume has to be absolute.'.format(container_path, section))

    if 'environment' in config and not isinstance(config['environment'], dict):
        errors.append('The environment variables should be described as a dictionary.')

    if errors:
        utils.log('The following errors were encountered while verifying the configuration:', err=True, fg='red', bold=True)
        for error in errors:
            utils.log('  - {}'.format(error), err=True, prefix=False)
        return False
    else:
        utils.info('The configuration has been verified without errors.')
        return True


def create_local_directory(local_path):
    """Create a local directory for a specified path that doesn't exist."""
    try:
        utils.debug('Creating a directory at the local path "{}".'.format(local_path))
        mkdir(local_path)
        utils.info('Created directory at "{}" as the path did not exist.'.format(local_path))
        return True
    except PermissionError:
        return False
