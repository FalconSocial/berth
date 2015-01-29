"""Handles the interface for working with FPM and package generation."""

import time

import berth.utils as utils


def package(config):
    """Package a project of some kind to a package of some kind."""
    utils.log('Packaging project.')

    volumes = config['package'].get('volumes', dict())
    volume_list, binds = utils.convert_volumes_list(volumes)

    command = list(map_to_fpm(config['package']['fpm']))
    utils.debug('Command to be run in packaging container is: {}'.format(str(command)))

    docker = utils.docker_client()
    container = docker.create_container(
        image=config['package'].get('image', 'dockerfile/fpm'),
        command=command,
        volumes=volume_list,
    )

    if container['Warnings']:
        utils.log('We got a warning when creating the packaging container:', err=True, fg='red', bold=True)
        utils.log(str(container['Warnings']), err=True, prefix=False)
        return False

    utils.debug('Starting packaging container.')
    start_time = time.time()
    docker.start(container['Id'], binds=binds)
    utils.info('Packaging container started.')

    exit_code = docker.wait(container['Id'])
    utils.info('The packaging container has stopped after {:.3} seconds.'.format(time.time() - start_time))

    if exit_code != 0 or utils.get_log_level() > 0:
        utils.debug('Getting output from container.')
        logs = docker.logs(container['Id']).decode('utf-8').rstrip()

        if exit_code != 0:
            utils.log('Packaging command failed with exit code: {}. Output follows:'.format(exit_code), err=True, fg='red', bold=True)
        else:
            utils.info('Packaging command output follows:')
        utils.log(logs, err=(exit_code != 0), prefix=False)
    else:
        utils.log('Packaging succeeded.')

    utils.debug('Removing packaging container.')
    docker.remove_container(container['Id'])
    utils.info('Removed packaging container.')

    return exit_code == 0


def map_to_fpm(config):  # pylint: disable = too-many-branches
    """Map settings in the YAML file to a FPM command."""
    yield 'fpm'
    arguments = []

    for key, value in config.items():
        param = create_parameter(key)

        if value is True:
            yield param

        elif isinstance(value, list):
            if key == '_arguments':
                for item in value:
                    arguments.append(str(item))

            else:
                for item in value:
                    yield param
                    yield str(item)

        elif isinstance(value, dict):
            if key == 'template-value':
                for template_key, template_value in value.items():
                    yield param
                    yield '{}={}'.format(template_key, template_value)

            elif key == 'deb-field':
                for field_key, field_value in value.items():
                    yield param
                    yield '{}: {}'.format(field_key, field_value)

            elif key == '_arguments':
                for file_key, file_value in value.items():
                    arguments.append('{}={}'.format(file_key, file_value))

            else:
                utils.log('The configuration item at package => fpm => {} was not understood and thus ignored.'.format(key))

        else:
            yield param
            yield str(value)

    for argument in arguments:
        yield argument


def create_parameter(key):
    """Make a command line parameter out of a key in a YAML file."""
    if len(key) == 1:
        return '-{}'.format(key)
    else:
        return '--{}'.format(key)
