"""Handles all command line actions for Berth."""

import berth.build as build
import berth.config as config
import berth.package as package
import berth.utils as utils
import click


@click.command(help='Berth use Docker containers to build packages for you, based on a YAML configuration file.')
@click.pass_context
@click.version_option(prog_name='Berth')
@click.argument('config_file', metavar='<CONFIG FILE>', type=click.File())
@click.option('-v', '--verbose', is_flag=True, help='Turn on verbose output.')
@click.option('-d', '--debug', is_flag=True, help='Turn on debug output.')
@click.option('-b', '--build-only', is_flag=True, help='Only perform the build step.')
@click.option('-p', '--package-only', is_flag=True, help='Only perform the package step.')
@click.option('-k', '--keep-containers', is_flag=True, help='Keep the containers around after they have been used.')
def main(context, config_file, verbose, debug, build_only, package_only, keep_containers):  # pylint: disable = too-many-arguments
    """Build a package."""
    if debug:
        utils.set_log_level(2)
    elif verbose:
        utils.set_log_level(1)

    if build_only and package_only:
        utils.log('--build-only and --package-only are mutually exclusive.', err=True, fg='red', bold=True)
        context.exit(1)

    configuration = config.read(config_file)

    if not configuration:
        context.exit(1)

    if not config.verify(configuration):
        context.exit(1)

    configuration['keep_containers'] = keep_containers

    if 'build' not in configuration:
        utils.info('No build configuration provided, skipping build.')
    elif package_only:
        utils.info('--package-only provided, skipping build.')
    else:
        if not utils.pull_image(configuration['build']['image']):
            context.exit(1)

        if not build.build(configuration):
            context.exit(1)

    if not utils.pull_image(configuration['package'].get('image', 'tenzer/fpm')):
        context.exit(1)

    if build_only:
        utils.info('--build-only provided, skipping packaging.')
    else:
        if not package.package(configuration):
            context.exit(1)

    utils.log('Done!')
    context.exit(0)


if __name__ == '__main__':
    main()  # pylint: disable = no-value-for-parameter
