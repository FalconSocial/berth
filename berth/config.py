"""Verifies the configuration provided."""

import berth.utils as utils
import yaml
import yaml.parser


def read(file_pointer):
    """Read the configuration file and parse the YAML contents."""
    utils.info('Reading the configuration file "{}"'.format(file_pointer.name))

    try:
        config = yaml.load(file_pointer.read())
    except yaml.parser.ParserError as error:
        utils.log('The configuration file could not be parsed:', err=True, fg='red', bold=True)
        utils.log(error.context, err=True, prefix=False)
        utils.log(str(error.context_mark), err=True, prefix=False)
        utils.log(error.problem, err=True, prefix=False)
        utils.log(str(error.problem_mark), err=True, prefix=False)
        return False

    utils.debug('Configuration parsed, contents:\n{}'.format(config))
    return config


def verify(config):
    """Verify the configuration contain the necessary details."""
    errors = []

    required = {
        'metadata': {
            'name',
        },
        'build': {
            'image',
            'script',
        },
        'package': {
            'version',
            'iteration',
            'output',
            'files',
        },
    }

    for section, fields in required.items():
        if not config.get(section):
            errors.append('A "{}" section is missing.'.format(section))
        else:
            for field in fields:
                if not config[section].get(field):
                    errors.append('"{}" is required in the {} section.'.format(field, section))

    if errors:
        utils.log('The following errors were encountered while verifying the configuration:', err=True, fg='red', bold=True)
        for error in errors:
            utils.log('  - {}'.format(error), err=True, prefix=False)
        return False
    else:
        utils.info('The configuration has been verified without errors.')
        return True
