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
def main(context, config_file, verbose, debug):
    """Build a package."""
    if debug:
        utils.set_log_level(2)
    elif verbose:
        utils.set_log_level(1)

    configuration = config.read(config_file)

    if not configuration:
        context.exit(1)

    if not config.verify(configuration):
        context.exit(1)

    if 'build' in configuration:
        if not utils.pull_image(configuration['build']['image']):
            context.exit(1)

        if not build.build(configuration):
            context.exit(1)

    if not utils.pull_image(configuration['package'].get('image', 'dockerfile/fpm')):
        context.exit(1)

    if not package.package(configuration):
        context.exit(1)

    utils.log('Done!')
    context.exit(0)


if __name__ == '__main__':
    main()  # pylint: disable = no-value-for-parameter
