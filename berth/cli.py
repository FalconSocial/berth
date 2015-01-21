"""Handles all command line actions for Berth."""

import berth.build as build
import berth.config as config
import berth.utils as utils
import click


@click.command(help='Berth use Docker containers to build packages for you, based on a YAML configuration file.')
@click.argument('config_file', metavar='<CONFIG FILE>', type=click.File())
@click.option('-v', '--verbose', is_flag=True, help='Turn on verbose output.')
@click.option('-d', '--debug', is_flag=True, help='Turn on debug output.')
def main(config_file, verbose, debug):
    """Build a package."""
    if debug:
        utils.set_log_level(2)
    elif verbose:
        utils.set_log_level(1)

    configuration = config.read(config_file)

    if not configuration:
        return

    if not config.verify(configuration):
        return

    build.build(configuration)


if __name__ == '__main__':
    main()  # pylint: disable = no-value-for-parameter
