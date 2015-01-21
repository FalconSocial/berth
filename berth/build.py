"""Handles everything related to Docker and the actual build process."""

import berth.utils as utils


def build(config):
    """Run the build part of the configuration."""
    utils.log('Building project.')
